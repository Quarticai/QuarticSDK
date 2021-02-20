from unittest import mock

from aloe import step, world

from quartic_sdk import APIClient
from quartic_sdk.core.entities import *
import quartic_sdk.utilities.test_helpers as TestHelpers
import quartic_sdk.utilities.constants as Constants


@step("we have successfully setup the client to test the methods")
def step_impl(context):
    """
    For the first step we setup the APIClient
    """
    world.client = APIClient("http://test_host", username="username", password="password")

@step("we call all the different possible methods in the entities")
def step_impl(context):
    """
    Now we step by step run all the possible methods that can be called by the users
    """
    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(TestHelpers.ASSET_LIST_GET)

        world.client_assets = world.client.assets()

    world.first_asset = world.client_assets.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(TestHelpers.TAG_LIST_GET)

        world.first_asset_tags = world.first_asset.get_tags()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(TestHelpers.BATCH_LIST_GET)

        world.first_asset_batches = world.first_asset.batches()

    world.first_tag = world.first_asset_tags.first()

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = TestHelpers.APIHelperCallAPI(TestHelpers.TAG_DATA_POST)

        world.first_tag_data = world.first_tag.data(start_time=1,stop_time=2)

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(TestHelpers.CONTEXT_FRAME_LIST_GET)

        world.context_frames = world.client.context_frames()

    world.first_context_frame = world.context_frames.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(TestHelpers.CONTEXT_FRAME_OCCURRENCE_GET)

        world.cf_occurrences = world.first_context_frame.occurrences()

@step("the methods works correctly resulting in correct data types")
def step_impl(context):
    """
    Now, we assert that the variables saved in the world are of the correct data types
    """
    assert isinstance(world.client_assets, EntityList)
    assert isinstance(world.first_asset, Asset)
    assert isinstance(world.first_asset_tags, EntityList)
    assert isinstance(world.first_tag, Tag)
    assert isinstance(world.first_asset_batches, EntityList)
    assert isinstance(world.first_asset_batches.first(), Batch)
    assert isinstance(world.context_frames, EntityList)
    assert isinstance(world.first_context_frame, ContextFrame)
    assert isinstance(world.cf_occurrences, EntityList)
    assert isinstance(world.cf_occurrences.first(), ContextFrameOccurrence)
