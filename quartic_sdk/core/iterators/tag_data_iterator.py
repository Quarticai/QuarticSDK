
import json
import pandas as pd
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.utilities.exceptions import IncorrectTransformationException


class TagDataIterator:
    """
    The given class is the iterator class, which will be used to iterate
    for getting the tag data values at the given intervals
    """

    def __init__(
            self,
            tags,
            start_time,
            stop_time,
            total_count,
            batch_size,
            api_helper,
            sampling_ratio=1,
            return_type=Constants.RETURN_JSON,
            wavelengths = {},
            transformations=[]):
        """
        We initialize the iterator with the given parameters
        :param tags: (BaseEntityList) Refers to the instance of BaseEntityList with
                each containing tags as the individual items
        :param start_time: (epoch) Start time of the query
        :param stop_time: (epoch) Stop time of the query
        :param count: Count of time ranges in this interval with each interval
                containing 200,000 points
        :param api_helper: (APIHelper) APIHelper class object
        :param cursor: Pagination cursor string
        :param sampling_ratio: The sampling_ratio at which the tag data is queried
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. If `transformation_type` is "aggregation", an optional key can be
            passed called `aggregation_timestamp`, which determines how the timestamp information
            will be retained after aggregation. Valid options are "first", "last" or "discard". By
            default, the last timestamp in each group will be retained.
            An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"},
                "aggregation_timestamp": "last",
            }]
        """

        TagDataIterator.raise_exception_for_transformation_schema(
            transformations, tags)

        self.total_count = total_count
        self.batch_size = batch_size
        self.tags = tags
        self.start_time = start_time
        self.stop_time = stop_time
        self.api_helper = api_helper
        self.sampling_ratio = sampling_ratio
        self.return_type = return_type
        self.wavelengths = wavelengths
        self._transformations = transformations
        self._cursor = None
        self._data_call_state = 0

    @staticmethod
    def raise_exception_for_transformation_schema(transformations, tags):
        """
        We validate the transformations schema. Its schema would be like the following:
        [{"transformation_type": "interpolation", "column": "1", "method": "linear"},
        {"transformation_type": "aggregation", "aggregation_column": "2",
        "aggregation_dict": {"1":{"1":"max"},"2":{"2":"std"}}}]
        :param transformations: List of transformations in the schema as above
        :param tags: List of tag ids
        :return: (None) Does not return anything, raises exception if validation fails
        """

        agg_transformation = [transformation for transformation in transformations if transformation.get(
            "transformation_type") == "aggregation"]
        if len(agg_transformation) > 1:
            raise IncorrectTransformationException(
                "Invalid transformations : Only one aggregation transformation can be applied at a time")
        for transformation in transformations:
            transformation_type = transformation.get("transformation_type")
            if transformation_type == "interpolation":
                if transformation.get("column") is None:
                    raise IncorrectTransformationException(
                        "Invalid transformations : Interpolation column is missing")
            elif transformation_type == "aggregation":
                if transformation.get("aggregation_column") is None \
                        or transformation.get("aggregation_dict") is None:
                    raise IncorrectTransformationException(
                        "Invalid transformations : aggregation_column and aggregation_dict is required")
                if len(transformation.get("aggregation_dict")
                       ) != tags.count() - 1:
                    raise IncorrectTransformationException(
                        "Invalid transformations : Aggregation for all columns not defined in aggregation_dict")
            else:
                raise IncorrectTransformationException(
                    "Invalid transformations : transformation_type is invalid")

    def create_post_data(self):
        """
        We create the required post data which will be used for making the POST call
        """
        return {
            "tags": [tag.id for tag in self.tags.all()],
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "sampling_ratio": self.sampling_ratio,
            "wavelengths" : self.wavelengths,
            "transformations": self._transformations,
            "batch_size": self.batch_size
        }

    def __iter__(self):
        """
        Return the data iterator with the data fetch state set at 0
        """
        self._data_call_state = 0
        return self

    def __next__(self):
        """
        Get the next object in the iteration.
        Note that the return object is inclusive of time ranges
        """
        if self._data_call_state != 0 and self._cursor is None:
            self._data_call_state = 0
            raise StopIteration
        if self._data_call_state == 0:
            body_json = self.create_post_data()
            tag_data_return = self.api_helper.call_api(
                Constants.RETURN_TAG_DATA, Constants.API_POST, body=body_json).json()
            self._data_call_state = 1
        else:
            tag_data_return = self.api_helper.call_api(
                url=Constants.RETURN_TAG_DATA,
                method_type=Constants.API_GET,
                query_params={
                    "cursor": self._cursor}).json()

        self._cursor = tag_data_return["cursor"]

        if self.return_type == Constants.RETURN_JSON:
            return tag_data_return["data"]

        tag_data_return_str = json.dumps(tag_data_return["data"])

        return pd.read_json(tag_data_return_str,
                                           orient="split",
                                           convert_dates=False,
                                           convert_axes=False)

    @classmethod
    def create_tag_data_iterator(
            cls,
            tags,
            start_time,
            stop_time,
            api_helper,
            sampling_ratio=1,
            return_type=Constants.RETURN_PANDAS,
            batch_size=Constants.DEFAULT_PAGE_LIMIT_ROWS,
            wavelengths = {},
            transformations=[]):
        """
        The method creates the TagDataIterator instance based upon the parameters that are passed here
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param sampling_ratio: sampling_ratio of the data
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param wavelengths: dict containing list of wavelengths(string) as value with key "wavelengths"
            Used for getting data for a spectral tag for specified wavelengths. 
            An example value here is:
            {"wavelengths:['1460000.0','1460001.0']}                                
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. If `transformation_type` is "aggregation", an optional key can be
            passed called `aggregation_timestamp`, which determines how the timestamp information
            will be retained after aggregation. Valid options are "first", "last" or "discard". By
            default, the last timestamp in each group will be retained.
            An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"},
                "aggregation_timestamp": "last",
            }]
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """

        TagDataIterator.raise_exception_for_transformation_schema(
            transformations, tags)
        body_json = {
            "tags": [tag.id for tag in tags.all()],
            "start_time": start_time,
            "stop_time": stop_time,
            "sampling_ratio": sampling_ratio,
            "wavelengths": wavelengths,
            "transformations": transformations,
            "batch_size": batch_size
        }
        if tags.count() == 0:
            raise Exception("There are no tags to fetch data of")
        tag_data_response = api_helper.call_api(
            Constants.RETURN_TAG_DATA,
            Constants.API_POST,
            body=body_json).json()
        return TagDataIterator(
            tags=tags,
            start_time=start_time,
            stop_time=stop_time,
            total_count=tag_data_response["total_count"],
            api_helper=api_helper,
            batch_size=batch_size,
            sampling_ratio=sampling_ratio,
            return_type=return_type,
            wavelengths = wavelengths,
            transformations=transformations)
