
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.iterators.tag_data_iterator import TagDataIterator


class Asset(Base):
    """
    The given class refers to the asset entity which is created based upon the
    asset object returned from the API
    """

    def __repr__(self):
        """
        Override the method to return the asset name with id
        """
        return f"<{Constants.ASSET_ENTITY}: {self.name}_{self.id}>"

    def get_tags(self):
        """
        The given method returns the list of tags for the given asset
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        tags_response = self.api_helper.call_api(
            Constants.GET_TAGS, Constants.API_GET, [self.id]).json()
        return EntityFactory(Constants.TAG_ENTITY, tags_response, self.api_helper)

    def event_frames(self):
        """
        The given method returns the list of event frames for the given asset
        """
        raise NotImplementedError

    def batches(self):
        """
        The given method returns the list of batches for the given asset
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        batches_response = self.api_helper.call_api(
            Constants.GET_BATCHES, Constants.API_GET, [self.id]).json()
        return EntityFactory(Constants.BATCH_ENTITY, batches_response, self.api_helper)

    def data(self, start_time, stop_time, granularity=0):
        """
        Get the data of all tags in the asset between the given start_time and
        stop_time for the given granularity
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param granularity: Granularity of the data
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        tags = self.get_tags()
        body_json = {
            "tags": [tag.id for tag in tags],
            "start_time": start_time,
            "stop_time": stop_time,
            "granularity": granularity
        }
        tag_data_response = self.api_helper.call_api(
            Constants.POST_TAG_DATA, Constants.API_POST, body=body_json)
        return TagDataIterator(tags, start_time, stop_time, tag_data_response["count"], self.api_helper)
