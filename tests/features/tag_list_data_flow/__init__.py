
import pandas as pd
import pytest
from unittest import mock
from aloe import step, world

from quartic_sdk import APIClient
from quartic_sdk.core.entities import Tag, Asset
from quartic_sdk.core.entity_helpers.entity_list import EntityList
from quartic_sdk.utilities.test_helpers import (
    APIHelperCallAPI,
    ASSET_LIST_GET,
    TAG_LIST_MULTI_GET,
    ASSET_DATA_POST,
    TAG_LIST_DATA_POST,
    JWT_TOKEN_RESPONSE
)
import quartic_sdk.utilities.constants as Constants


@step("we have successfully set up client to test tags data flow")
def step_impl(context):
    """
    For the first step we setup the APIClient, and the related tag_list
    """
    with mock.patch('requests.post') as jwt_requests_post:
        jwt_requests_post.return_value = APIHelperCallAPI(
            JWT_TOKEN_RESPONSE)
        world.client = APIClient(
            "http://test_host",
            username="username",
            password="password")
        world.tag_list = EntityList(Constants.TAG_ENTITY)


@step("we call the required methods to get the tags list data")
def step_impl(context):
    """
    Now we call the different internal methods and save their values
    internally in the world parameter
    """

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(ASSET_LIST_GET)

        world.client_assets = world.client.assets()

    world.first_asset = world.client_assets.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(TAG_LIST_MULTI_GET)

        world.first_asset_tags = world.first_asset.get_tags()

    world.tag_list.add(world.first_asset_tags.get("id", 1))
    world.tag_list.add(world.first_asset_tags.get("id", 2))

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(TAG_LIST_DATA_POST)

        world.tag_list_data_pd = world.tag_list.data(start_time=1, stop_time=2)

        world.tag_list_data_json = world.tag_list.data(
            start_time=1, stop_time=2, return_type=Constants.RETURN_JSON)

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(TAG_LIST_DATA_POST)

        test_transformation1 = [{
            "transformation_type": "interpolation",
            "column": "1",
            "method": "linear"
        }, {
            "transformation_type": "interpolation",
            "column": "2",
            "method": "cubic",
            "order": 2
        }]

        world.first_asset_data_with_correct_transformation = world.tag_list.data(
            start_time=1, stop_time=2, transformations=test_transformation1)


@step("the return of tag list data works correctly for json and pandas df")
def step_impl(context):
    """
    In this step we assert to ensure that the methods call the correct functions
    to ensure the correct variable types and the respective data created
    """

    with pytest.raises(Exception):
        world.tag_list.add(world.first_asset)

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(
            TAG_LIST_DATA_POST.copy())
        assert isinstance(world.tag_list_data_pd, pd.DataFrame)

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(
            TAG_LIST_DATA_POST.copy())
        assert isinstance(world.tag_list_data_json, dict)

    with pytest.raises(Exception):
        test_transformation2 = [{
            "transformation_type": "interpolation",
            "method": "linear"
        }]
        world.tag_data_with_incorrect_transformation = world.tag_list.data(
            start_time=1, stop_time=2, transformations=test_transformation2)

    with pytest.raises(Exception):
        test_transformation3 = [{
            "transformation_type": "interpolation",
            "column": "1",
            "method": "linear"
        }, {
            "transformation_type": "aggregation",
            "aggregation_column": "1"
        }]

        world.tag_data_with_incorrect_transformation = world.tag_list.data(
            start_time=1, stop_time=2, transformations=test_transformation3)
