
from quartic_sdk.api.api_helpers import APIHelpers
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory


class APIClient:

    def __init__(self, host, username=None, password=None, oauth_token=None, verify_ssl=None):
        """
        Create the API Client
        """
        self.api_helper = APIHelpers(host, username, password, oauth_token, verify_ssl)

    @staticmethod
    def version():
        """
        Return the SDK version
        """
        exec(open("./_version.py", "r").read())
        return None

    def assets(self):
        """
        Get the assets method
        """
        return_json = self.api_helper.call_api(
            Constants.GET_ASSETS, Constants.API_GET).json()
        return EntityFactory(Constants.ASSET_ENTITY, return_json, self.api_helper)

    def process_units(self):
        """
        Get the process units
        """
        raise NotImplementedError

    def work_cells(self):
        """
        Get the work cells
        """
        raise NotImplementedError

    def tags(self, asset_id):
        """
        Get the tags
        """
        return_json = self.api_helper.call_api(
            Constants.GET_TAGS, Constants.API_GET, [asset_id]).json()
        return EntityFactory(Constants.TAG_ENTITY, return_json, self.api_helper)
