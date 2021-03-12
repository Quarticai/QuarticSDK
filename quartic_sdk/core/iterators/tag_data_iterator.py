
import json
import pandas as pd
import quartic_sdk.utilities.constants as Constants


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
            count,
            api_helper,
            offset=0,
            granularity=0,
            return_type=Constants.RETURN_JSON,
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
        :param offset: Current offset
        :param granularity: The granularity at which the tag data is queried
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"}
            }]
        """
        if not TagDataIterator.validate_transformations_schema(
                transformations, tags):
            raise Exception("Invalid transformations")
        self.count = count
        self._offset = offset
        self.tags = tags
        self.start_time = start_time
        self.stop_time = stop_time
        self.api_helper = api_helper
        self.granularity = granularity
        self.return_type = return_type
        self._transformations = transformations

    @staticmethod
    def validate_transformations_schema(transformations, tags):
        """
        We validate the transformations schema. Its schema would be like the following:
        [{"transformation_type": "interpolation", "column": "1", "method": "linear"},
        {"transformation_type": "aggregation", "aggregation_column": "2",
        "aggregation_dict": {"1":{"1":"max"},"2":{"2":"std"}}}]
        :param transformations: List of transformations in the schema as above
        :param tags: List of tag ids
        :return: (bool) Whether the transformation schema is valid
        """
        if not transformations:
            return True
        agg_transformation = [transformation for transformation in transformations if transformation.get(
            "transformation_type") == "aggregation"]
        if len(agg_transformation) > 1:
            return False
        for transformation in transformations:
            transformation_type = transformation.get("transformation_type")
            if transformation_type == "interpolation":
                if transformation.get("column") is None:
                    return False
            elif transformation_type == "aggregation":
                if transformation.get("aggregation_column") is None \
                        or transformation.get("aggregation_dict") is None:
                    return False
                if len(transformation.get("aggregation_dict")
                       ) != tags.count() - 1:
                    return False
            else:
                return False
        return True

    def create_post_data(self):
        """
        We create the required post data which will be used for making the POST call
        """
        return {
            "tags": [tag.id for tag in self.tags.all()],
            "start_time": self.start_time,
            "stop_time": self.stop_time,
            "granularity": self.granularity,
            "transformations": self._transformations
        }

    def __next__(self):
        """
        Get the next object in the iteration
        """
        if self._offset >= self.count:
            raise StopIteration
        body_json = self.create_post_data()
        tag_data_return = self.api_helper.call_api(
            Constants.POST_TAG_DATA, Constants.API_POST, query_params={
                "offset": self._offset}, body=body_json).json()
        self._offset += 1

        del tag_data_return['count']
        del tag_data_return['offset']

        if self.return_type != Constants.RETURN_JSON:
            tag_data_return_str = json.dumps(tag_data_return)

            tag_data_return = pd.read_json(tag_data_return_str,
                                           orient="split",
                                           convert_dates=False,
                                           convert_axes=False)

        return tag_data_return

    def __getitem__(self, key):
        """
        We override this method to get the object at the given key
        """
        if key >= self.count:
            raise IndexError
        body_json = self.create_post_data()
        tag_data_return = self.api_helper.call_api(
            Constants.POST_TAG_DATA, Constants.API_POST, query_params={
                "offset": key}, body=body_json).json()

        del tag_data_return['count']
        del tag_data_return['offset']

        if self.return_type != Constants.RETURN_JSON:
            tag_data_return_str = json.dumps(tag_data_return)

            tag_data_return = pd.read_json(tag_data_return_str,
                                           orient="split",
                                           convert_dates=False,
                                           convert_axes=False)

        return tag_data_return

    @classmethod
    def create_tag_data_iterator(
            cls,
            tags,
            start_time,
            stop_time,
            api_helper,
            granularity=0,
            return_type=Constants.RETURN_PANDAS,
            transformations=[]):
        """
        The method creates the TagDataIterator instance based upon the parameters that are passed here
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param granularity: Granularity of the data
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"}
            }]
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        if not TagDataIterator.validate_transformations_schema(
                transformations, tags):
            raise Exception("Invalid transformations")
        body_json = {
            "tags": [tag.id for tag in tags.all()],
            "start_time": start_time,
            "stop_time": stop_time,
            "granularity": granularity,
            "transformations": transformations
        }
        if tags.count() == 0:
            raise Exception("There are no tags to fetch data of")
        tag_data_response = api_helper.call_api(
            Constants.POST_TAG_DATA, Constants.API_POST, body=body_json).json()
        return TagDataIterator(
            tags=tags,
            start_time=start_time,
            stop_time=stop_time,
            count=tag_data_response["count"],
            api_helper=api_helper,
            granularity=granularity,
            return_type=return_type,
            transformations=transformations)
