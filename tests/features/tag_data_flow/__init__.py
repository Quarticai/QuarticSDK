
import pytest
from unittest import mock

from aloe import step, world

from quartic_sdk import APIClient
from quartic_sdk.core.entities import Tag, Asset
from quartic_sdk.core.entity_helpers.entity_list import EntityList
from quartic_sdk.utilities.test_helpers import (
    APIHelperCallAPI,
    ASSET_LIST_GET,
    TAG_LIST_GET,
    TAG_DATA_POST,
    JWT_TOKEN_RESPONSE
)


@step("we have successfully set up client to test tag data flow")
def step_impl(context):
    """
    For the first step we setup the APIClient
    """
    with mock.patch('requests.post') as jwt_requests_post:
        jwt_requests_post.return_value = APIHelperCallAPI(
            JWT_TOKEN_RESPONSE)
        world.client = APIClient(
            "http://test_host",
            username="username",
            password="password")


@step("we call the required methods to get the tag details")
def step_impl(context):
    """
    Now we call the different internal methods to get tag data
    """

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(ASSET_LIST_GET)

        world.client_assets = world.client.assets()

    world.first_asset = world.client_assets.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(TAG_LIST_GET)

        world.first_asset_tags = world.first_asset.get_tags()

    world.first_tag = world.first_asset_tags.first()

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(TAG_DATA_POST)

        world.tag_data_without_transformation = world.first_tag.data(
            start_time=1, stop_time=2)

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(TAG_DATA_POST)

        test_transformation1 = [{
            "transformation_type": "interpolation",
            "column": "1",
            "method": "linear"
        }]

        world.tag_data_with_correct_transformation = world.first_tag.data(
            start_time=1, stop_time=2, transformations=test_transformation1)


@step("the return of tag data works correctly for json and pandas df")
def step_impl(context):
    """
    In this step we assert to ensure that the methods call the correct functions
    to ensure the correct variable types and the respective data created for a single data
    """
    assert isinstance(world.first_tag, Tag)
    assert world.first_tag.id == TAG_LIST_GET[0]["id"]

    with pytest.raises(Exception):
        test_transformation2 = [{
            "transformation_type": "interpolation",
            "method": "linear"
        }]

        world.tag_data_with_incorrect_transformation = world.first_tag.data(
            start_time=1, stop_time=2, transformations=test_transformation2)

    with pytest.raises(Exception):
        test_transformation3 = [{
            "transformation_type": "transform",
            "method": "linear",
            "column": "1"
        }]
        world.tag_data_with_incorrect_transformation_type = world.first_tag.data(
            start_time=1, stop_time=2, transformations=test_transformation3)
