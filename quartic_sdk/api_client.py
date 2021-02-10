
from quartic_sdk.api.api_helpers import APIHelpers
from quartic_sdk.utilities.constants import (
    GET_ASSETS,
    GET_CONTEXT_FRAME_DEFINITIONS,
    GET_TAGS,
    POST_TAG_DATA,
    GET_CONTEXT_FRAME_OCCURRENCES,
    GET_BATCHES
)


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
        return self.api_helper.call_api(
            GET_ASSETS, "GET").json()

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
        return self.api_helper.call_api(
            GET_TAGS, [asset_id]).json()
