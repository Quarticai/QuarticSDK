"""
The given file contains the class to refer to the asset entity
"""
import logging
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.utilities.tag_data import TagData


class Asset(Base):
    """
    The given class refers to the asset entity which is created based upon the
    asset object returned from the API
    """

    mapping = {
        "status": Constants.STATUS
    }

    def __repr__(self):
        """
        Override the method to return the asset name
        """
        return f"<{Constants.ASSET_ENTITY}: {self.name}>"

    def get_tags(self, query_params={}):
        """
        The given method returns the list of tags for the given asset
        :param query_params: Dictionary of filter conditions
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        query_params["asset"] = self.id
        tags_response = self.api_helper.call_api(
            Constants.GET_TAGS,
            Constants.API_GET,
            path_params=[],
            query_params=query_params).json()
        return EntityFactory(
            Constants.TAG_ENTITY,
            tags_response,
            self.api_helper)

    def event_frames(self, query_params={}):
        """
        The given method returns the list of event frames for the given asset
        :param query_params: Dictionary of filter conditions
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        query_params["asset"] = self.id
        event_frame_response = self.api_helper.call_api(
            Constants.GET_EVENT_FRAMES,
            Constants.API_GET,
            query_params=query_params).json()
        return EntityFactory(
            Constants.EVENT_FRAME_ENTITY,
            event_frame_response,
            self.api_helper)

    def batches(self, query_params={}):
        """
        The given method returns the list of batches for the given asset
        :param query_params: Dictionary of filter conditions
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        batches_response = self.api_helper.call_api(
            Constants.GET_BATCHES, Constants.API_GET, [self.id], query_params).json()
        return EntityFactory(
            Constants.BATCH_ENTITY,
            batches_response,
            self.api_helper)

    def data(self, start_time, stop_time, interval_min=1, aggregation_type="last", wide_df=True, return_type=Constants.RETURN_PANDAS,
             transformations=[]):
        """
        Get the data of all tags in the asset between the given start_time and
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
        tags = self.get_tags().exclude(
            tag_data_type=Constants.TAG_DATA_TYPES[Constants.SPECTRAL])
        logging.info("Filtering to fetch data only for non-spectral tags")
        return TagData.get_tag_data(tags=tags, start_time=start_time, stop_time=stop_time, api_helper=self.api_helper,
                                    interval_min=interval_min, aggregation_type=aggregation_type, return_type=return_type,
                                    wide_df=wide_df, transformations=transformations)

    def __getattribute__(self, name):
        """
        This method overrides the python's object __getattribute__ method. This is used to
        map some constant value of an object to some meaningful string constants for better
        readability
        :param name: name of the object attribute we want to access for example asset.status
        :return: Either mapped value or raw value with respect to the object attribute
        """
        asset_mapping = Asset.mapping
        if name in asset_mapping.keys() and asset_mapping[name].get(
                self.__dict__[name]):
            return asset_mapping[name][self.__dict__[name]]
        return object.__getattribute__(self, name)
