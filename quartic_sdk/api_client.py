from typing import List, Dict


import quartic_sdk.utilities.constants as Constants
from quartic_sdk.api.api_helper import APIHelper
from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
from quartic_sdk._version import __version__


class APIClient:

    def __init__(
            self,
            host,
            username=None,
            password=None,
            oauth_token=None,
            cert_path=None,
            verify_ssl=True):
        """
        Create the API Client
        """
        self.api_helper = APIHelper(
            host, username, password, oauth_token, cert_path, verify_ssl)

    @staticmethod
    def version():
        """
        Return the SDK version
        """
        return __version__

    def assets(self):
        """
        Get the assets method
        """
        return_json = self.api_helper.call_api(
            Constants.GET_ASSETS, Constants.API_GET).json()
        return EntityFactory(
            Constants.ASSET_ENTITY,
            return_json,
            self.api_helper)

    def context_frames(self):
        """
        Get the context frames method
        :return: (EntityList) List of context frames
        """
        return_json = self.api_helper.call_api(
            Constants.GET_CONTEXT_FRAME_DEFINITIONS, Constants.API_GET).json()
        return EntityFactory(
            Constants.CONTEXT_FRAME_ENTITY,
            return_json,
            self.api_helper)

    def edge_connectors(self):
        """
        Get the edge connectors method
        """
        return_json = self.api_helper.call_api(
            Constants.GET_EDGE_CONNECTORS, Constants.API_GET).json()
        return EntityFactory(Constants.EDGE_CONNECTOR_ENTITY, return_json, self.api_helper)

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
        :param asset_id: ID of the asset
        :return: (EntityList) List of tags belonging to the asset
        """
        return_json = self.api_helper.call_api(
            Constants.GET_TAGS, Constants.API_GET, path_params=[], query_params={"asset": asset_id}).json()
        return EntityFactory(
            Constants.TAG_ENTITY,
            return_json,
            self.api_helper)

    def list_models(
            self,
            is_active: bool = None,
            ml_node: int = None) -> List[Dict]:
        """
        List models and its parameters accessible by user
        :param is_active: Boolean Indicator if list should contain active nodes or not
        :param ml_node:   Ml Node id to filter models deployed to particular node
        :return:          list of dictionary
        """
        query_params = {}
        if is_active is not None:
            query_params['is_active'] = is_active
        if ml_node:
            query_params['ml_node'] = ml_node
        response = self.api_helper.call_api(
            Constants.CMD_MODEL_ENDPOINT,
            method_type='GET',
            path_params=[],
            query_params=query_params,
            body={})
        response.raise_for_status()
        return EntityFactory(
            Constants.MODEL_ENTITY,
            response.json(),
            self.api_helper)
