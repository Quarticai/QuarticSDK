import quartic_sdk.utilities.constants as Constants
from quartic_sdk.api.api_helper import APIHelper
from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
from quartic_sdk._version import __version__
from quartic_sdk.utilities.exceptions import IncorrectParameterException


class APIClient:

    def __init__(
            self,
            host,
            username=None,
            password=None,
            oauth_token=None,
            cert_path=None,
            verify_ssl=True,
            gql_host=None):
        """
        Create the API Client
        """
        self.api_helper = APIHelper(
            host, username, password, oauth_token, cert_path, verify_ssl, gql_host)

    @staticmethod
    def version():
        """
        Return the SDK version
        """
        return __version__

    def assets(self, query_params={}):
        """
        Get the assets method
        :param query_params: Dictionary of filter conditions
        """
        return_json = self.api_helper.call_api(
            Constants.GET_ASSETS, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(
            Constants.ASSET_ENTITY,
            return_json,
            self.api_helper)

    def context_frames(self, query_params={}):
        """
        Get the context frames method
        :param query_params: Dictionary of filter conditions
        :return: (EntityList) List of context frames
        """
        return_json = self.api_helper.call_api(
            Constants.GET_CONTEXT_FRAME_DEFINITIONS, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(
            Constants.CONTEXT_FRAME_ENTITY,
            return_json,
            self.api_helper)

    def edge_connectors(self, query_params={}):
        """
        Get the edge connectors method
        :param query_params: Dictionary of filter conditions
        """

        query_params['parent__isnull'] = True
        return_json = self.api_helper.call_api(
            Constants.GET_EDGE_CONNECTORS, Constants.API_GET, query_params=query_params).json()
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

    def tags(self, asset_id, query_params={}):
        """
        Get the tags
        :param asset_id: ID of the asset
        :param query_params: Dictionary of filter conditions
        :return: (EntityList) List of tags belonging to the asset
        """
        query_params["asset"] = asset_id
        return_json = self.api_helper.call_api(
            Constants.GET_TAGS, Constants.API_GET, path_params=[], query_params=query_params).json()
        return EntityFactory(
            Constants.TAG_ENTITY,
            return_json,
            self.api_helper)

    def event_frames(self, query_params={}):
        """
        Get the Event Frames
        :param query_params: Dictionary of filter conditions
        :return: (EntityList) List of Event Frames belonging to the asset
        """
        return_json = self.api_helper.call_api(
            Constants.GET_EVENT_FRAMES, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(Constants.EVENT_FRAME_ENTITY, return_json, self.api_helper)

    def list_models(
            self,
            is_active: bool = None,
            ml_node: int = None,
            model_type: int = Constants.MODEL_TYPE_TELEMETRY,
            query_params={}):
        """
        List models and its parameters accessible by user

        :param is_active: Boolean Indicator if list should contain active nodes or not
        :param ml_node:   Ml Node id to filter models deployed to particular node
        :param model_type: Ml model type. 0 - All models , 1 - Telemetry models (Default) , 2 - Spectral models
        :param query_params: Dictionary of filter conditions
        :return:          list of dictionary
        """
        if model_type not in Constants.MODEL_TYPE.keys():
            raise IncorrectParameterException(f"Valid model_type values are {Constants.MODEL_TYPE.keys()}. "
                                              f"InValid value supplied - {model_type}")
        if is_active is not None:
            query_params['is_active'] = is_active
        if ml_node:
            query_params['ml_node'] = ml_node
        query_params['model_type'] = model_type

        response = self.api_helper.call_api(
            Constants.CMD_MODEL_ENDPOINT,
            method_type=Constants.API_GET,
            path_params=[],
            query_params=query_params,
            body={})

        response.raise_for_status()
        return EntityFactory(
            Constants.MODEL_ENTITY,
            response.json(),
            self.api_helper)

    def products(self, query_params={}):
        """
        This method is used to fetch list of all product belongs to a particular client
        :param query_params: Dictionary of filter conditions
        :return: Product(Product Entity) Objects
        """
        return_json = self.api_helper.call_api(
            Constants.GET_PRODUCTS, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(Constants.PRODUCT_ENTITY, return_json, self.api_helper)

    def sites(self, query_params={}):
        """
        This method is used to fetch all sites available for a user's client
        :param query_params: Dictionary of filter conditions
        :return: Site(Site Entity) Objects
        """
        return_json = self.api_helper.call_api(
            Constants.GET_SITES, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(Constants.SITE_ENTITY, return_json, self.api_helper)
