
from unittest import mock
import pytest
import pandas as pd
from aloe import step, world

from quartic_sdk import APIClient
from quartic_sdk.core.entities import Tag, EdgeConnector
from quartic_sdk.core.entity_helpers.entity_list import EntityList
from quartic_sdk.utilities.test_helpers import (
    APIHelperCallAPI,
    EDGE_CONNECTOR_LIST_GET,
    TAG_LIST_GET,
    EDGE_CONNECTOR_DATA_POST,
    TAG_LIST_MULTI_GET,
    JWT_TOKEN_RESPONSE
)
import quartic_sdk.utilities.constants as Constants


@step("we have successfully set up client to test data source data flow")
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


@step("we call the required methods to get the data souce data")
def step_impl(context):
    """
    Now we call the different internal methods and save their values
    internally in the world parameter
    """

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(EDGE_CONNECTOR_LIST_GET)

        world.client_edge_connectors = world.client.edge_connectors()

    world.first_edge_connector = world.client_edge_connectors.first()

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(EDGE_CONNECTOR_DATA_POST)

        with mock.patch('requests.get') as requests_get:
            requests_get.return_value = APIHelperCallAPI(TAG_LIST_MULTI_GET)

            # return type default is pandas dataframe
            world.first_edge_connector_data_pd = world.first_edge_connector.data(
                start_time=1, stop_time=2)

            world.first_edge_connector_data_json = world.first_edge_connector.data(
                start_time=1, stop_time=2, return_type=Constants.RETURN_JSON)

    test_transformation1 = [{
        "transformation_type": "interpolation",
        "column": "1",
        "method": "linear"
    }]

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = APIHelperCallAPI(EDGE_CONNECTOR_DATA_POST)

        with mock.patch('requests.get') as requests_get:
            requests_get.return_value = APIHelperCallAPI(TAG_LIST_MULTI_GET)

            # return type default is pandas dataframe
            world.first_edge_connector_data_with_correct_transformation_pd = world.first_edge_connector.data(
                start_time=1, stop_time=2, transformations=test_transformation1)

            world.first_edge_connector_data_with_correct_transformation_json = world.first_edge_connector.data(
                start_time=1,
                stop_time=2,
                transformations=test_transformation1,
                return_type=Constants.RETURN_JSON)

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = APIHelperCallAPI(TAG_LIST_MULTI_GET)

        test_transformation2 = [{
            "transformation_type": "interpolation",
            "method": "linear"
        }]

        with pytest.raises(Exception):
            world.tag_data_with_incorrect_transformation = world.first_edge_connector.data(
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

            world.tag_data_with_incorrect_transformation = world.first_edge_connector.data(
                start_time=1, stop_time=2, transformations=test_transformation3)


@step("the return of data source data works correctly for json and pandas df")
def step_impl(context):
    """
    In this step we assert to ensure that the methods call the correct functions
    to ensure the correct variable types and the respective data created
    """
    assert isinstance(world.client_edge_connectors, EntityList)
    assert world.client_edge_connectors.first().id == EDGE_CONNECTOR_LIST_GET[0]["id"]

    assert isinstance(world.first_edge_connector, EdgeConnector)
    assert world.first_edge_connector.id == EDGE_CONNECTOR_LIST_GET[0]["id"]

    with mock.patch('requests.post') as requests_post1:
        requests_post1.return_value = APIHelperCallAPI(EDGE_CONNECTOR_DATA_POST.copy())
        assert isinstance(world.first_edge_connector_data_pd, pd.DataFrame)

    with mock.patch('requests.post') as requests_post2:
        requests_post2.return_value = APIHelperCallAPI(EDGE_CONNECTOR_DATA_POST.copy())
        assert isinstance(world.first_edge_connector_data_json, dict)

    with mock.patch('requests.post') as requests_post3:
        requests_post3.return_value = APIHelperCallAPI(EDGE_CONNECTOR_DATA_POST.copy())
        assert isinstance(world.first_edge_connector_data_with_correct_transformation_pd, pd.DataFrame)

    with mock.patch('requests.post') as requests_post4:
        requests_post4.return_value = APIHelperCallAPI(EDGE_CONNECTOR_DATA_POST.copy())
        assert isinstance(world.first_edge_connector_data_with_correct_transformation_json, dict)
