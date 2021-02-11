from behave import *
from quartic_sdk import *
from unittest.mock import Mock, patch
import requests


client = None
client_assets = None
first_asset_tags = None

@given("we have successfully set up client and mocked requests method")
def step_impl(context):
    client = APIClient("test_host", username="username", password="password")


@when("we call different internal methods")
def step_impl(context):
    # requests.get = Mock(return_value)

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = [{"id": 1, "name": "Asset_name", "edge_connectors": [1,2]}]
