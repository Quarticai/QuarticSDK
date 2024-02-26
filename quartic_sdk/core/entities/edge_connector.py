from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.utilities.tag_data import TagData
from quartic_sdk.core.iterators.historical_tag_data_iterator import HistoricalTagDataIterator


class EdgeConnector(Base):
    """
    The given class refers to the data source entity which is created based upon the
    data source object returned from the API
    """

    mapping = {
        "status": Constants.STATUS,
        'connector_protocol': Constants.CONNECTOR_PROTOCOLS,
        "stream_status": Constants.STATUS,
    }

    def __repr__(self):
        """
        Override the method to return the data source name
        """
        return f"<{Constants.EDGE_CONNECTOR_ENTITY}: {self.name}>"

    def get_tags(self, query_params={}):
        """
        The given method returns the list of tags for the given asset
        :param query_params: Dictionary of filter conditions
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        tag_query_params = {**query_params}
        if (
            self.connector_protocol == Constants.CONNECTOR_PROTOCOLS[Constants.SQL]
            and self.parent is None
        ):
            tag_query_params["edge_connector__parent"] = self.id
        else:
            tag_query_params["edge_connector"] = self.id
        tags_response = self.api_helper.call_api(
            Constants.GET_TAGS, Constants.API_GET, path_params=[], query_params=tag_query_params).json()
        return EntityFactory(Constants.TAG_ENTITY, tags_response, self.api_helper)

    def historical_data(self,
        start_time,
        stop_time,
        batch_size=Constants.DEFAULT_BATCH_SIZE,
        max_records=None,
        tags=None,
        return_type=Constants.RETURN_PANDAS):
        """
        Fetch historical data for the given OPCUA edge connector
        """
        if not tags:
            tags = self.get_tags()
        return HistoricalTagDataIterator(tags, self.id, start_time, stop_time, self.api_helper, batch_size, max_records,
            return_type)

    def data(self, start_time, stop_time, interval_min=1, aggregation_type="last", wide_df=True, return_type=Constants.RETURN_PANDAS,
             transformations=[]):
        """
        Get the data of all tags in the edge connector between the given start_time and
        stop_time for the given interval duration
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param interval_min: (int) The interval duration in minutes for downsampling the data
        :param aggregation_type: (str) The aggregation function to be used for the query. (Valid values: first, last)
        :param wide_df: (bool) If the response is needed in wide or long format. Defaults to True.
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
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        tags = self.get_tags()
        return TagData.get_tag_data(tags=tags, start_time=start_time, stop_time=stop_time, api_helper=self.api_helper,
                                    interval_min=interval_min, aggregation_type=aggregation_type, return_type=return_type,
                                    wide_df=wide_df, transformations=transformations)

    def __getattribute__(self, name):
        """
        This method overrides the python's object __getattribute__ method. This is used to
        map some constant value of an object to some meaningful string constants for better
        readability
        :param name: name of the object attribute we want to access for example edge_connector.connector_protocol
        :return: Either mapped value or raw value with respect to the object attribute
        """
        edge_connector_mapping = EdgeConnector.mapping
        if name in edge_connector_mapping.keys() and edge_connector_mapping[name].get(self.__dict__[name]):
            return edge_connector_mapping[name][self.__dict__[name]]
        return object.__getattribute__(self, name)
