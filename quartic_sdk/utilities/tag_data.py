
import pandas as pd
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.utilities.exceptions import IncorrectTransformationException


class TagData:
    """
    This helper class is used for getting tag data by calling tagdata cursor api
    """

    def __init__(
            self,
            tags,
            start_time,
            stop_time,
            api_helper,
            return_type=Constants.RETURN_PANDAS,
            wavelengths = [],
            transformations=[]):
        """
        We initialize the class with the given parameters
        :param tags: (BaseEntityList) Refers to the instance of BaseEntityList with
                each containing tags as the individual items
        :param start_time: (epoch) Start time of the query
        :param stop_time: (epoch) Stop time of the query
        :param count: Count of time ranges in this interval with each interval
                containing 200,000 points
        :param api_helper: (APIHelper) APIHelper class object
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

        TagData.raise_exception_for_transformation_schema(
            transformations, tags)

        self.tags = tags
        self.start_time = start_time
        self.stop_time = stop_time
        self.api_helper = api_helper
        self.return_type = return_type
        self.wavelengths = wavelengths
        self._transformations = transformations
        self.offset_map = {}

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

    @classmethod
    def get_tag_data(cls, tags, start_time, stop_time, api_helper, interval_min=1, aggregation_type="last",
                     wide_df=True, return_type=Constants.RETURN_PANDAS, wavelengths=[], transformations=[]):
        """
        The method gets the tag data based upon the parameters that are passed here
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param interval_min: (int) The interval duration in minutes for downsampling the data
        :param aggregation_type: (str) The aggregation function to be used for the query. (Valid values: first, last)
        :param wide_df: (bool) If the response is needed in wide or long format. Defaults to True.
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
        cls.raise_exception_for_transformation_schema(
            transformations, tags)
        if tags.count() == 0:
            raise Exception("There are no tags to fetch data of")
        body_json = {
            "tags": [tag.id for tag in tags.all()],
            "start_time": start_time,
            "stop_time": stop_time,
            "wavelengths": wavelengths,
            "transformations": transformations,
            "interval": interval_min, 
            "aggregation_type": aggregation_type,
            "wide_df": wide_df,
        }
        tag_data_return = api_helper.call_api(
                Constants.RETURN_TAG_DATA, Constants.API_POST, body=body_json).json()
        if return_type == Constants.RETURN_JSON:
                return tag_data_return["data"]
        return pd.DataFrame(
            tag_data_return["data"]["data"],
            index=tag_data_return["data"]["index"],
            columns=tag_data_return["data"]["columns"],
        )
