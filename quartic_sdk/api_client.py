from typing import List, Dict

import cloudpickle

from quartic_sdk.api.api_helpers import APIHelpers
from quartic_sdk.utilities.constants import LIST_MODELS_ENDPOINT, GET_MODEL_ENDPOINT
from ._version import __version__
from quartic_sdk.utilities.constants import (
    GET_ASSETS,
    GET_CONTEXT_FRAME_DEFINITIONS,
    GET_TAGS,
    POST_TAG_DATA,
    GET_CONTEXT_FRAME_OCCURRENCES,
    GET_BATCHES
)
from .model.helpers import ModelUtils


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

    def list_models(self, is_active: bool = None, ml_node: int = None) -> List[Dict]:
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

        print(query_params)
        response = self.api_helper.call_api(LIST_MODELS_ENDPOINT, method_type='GET',
                                            path_params=[], query_params=query_params, body={})
        response.raise_for_status()
        return response.json()

    def get_model(self, model_id: str) -> Dict:
        """
        Fetches model object and model parameters for given model id
        :param model_id: Id of the model to fetch
        :return:        Dictionary
        """
        response = self.api_helper.call_api(GET_MODEL_ENDPOINT, method_type='GET',
                                            path_params=[model_id],
                                            query_params={},
                                            body={})
        response.raise_for_status()
        data = response.json()
        model_string = response.json()['model']
        checksum_received = model_string[:32]
        model = cloudpickle.loads(model_string[32:].encode())

        assert ModelUtils.get_checksum(model.encode()) == checksum_received
        data['model'] = model

        return data
