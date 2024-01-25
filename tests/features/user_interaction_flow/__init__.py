
from unittest import mock

from aloe import step, world
from pandas.core.indexes.numeric import Int64Index

from quartic_sdk import APIClient
from quartic_sdk.core.entities import *
from quartic_sdk.core.entity_helpers.entity_list import EntityList
import quartic_sdk.utilities.test_helpers as TestHelpers
import quartic_sdk.utilities.constants as Constants


@step("we have successfully setup the client to test the methods")
def step_impl(context):
    """
    For the first step we setup the APIClient
    """
    with mock.patch('requests.post') as jwt_requests_post:
        jwt_requests_post.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.JWT_TOKEN_RESPONSE)
        world.client = APIClient(
            "http://test_host",
            username="username",
            password="password")


@step("we call all the different possible methods in the entities")
def step_impl(context):
    """
    Now we step by step run all the possible methods that can be called by the users
    """
    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.ASSET_LIST_GET)

        world.client_assets = world.client.assets()

    world.first_asset = world.client_assets.first()
    world.assets_excluding_first = world.client_assets.exclude(
        id=world.first_asset.id)
    world.assets_filtered = world.client_assets.filter(id=world.first_asset.id)

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.TAG_LIST_GET)

        world.client_asset_tags = world.client.tags(world.first_asset.id)

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.TAG_LIST_GET)

        world.first_asset_tags = world.first_asset.get_tags()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.BATCH_LIST_GET)

        world.first_asset_batches = world.first_asset.batches()

    world.first_tag = world.first_asset_tags.first()

    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.TAG_DATA_POST)

        world.first_tag_data = world.first_tag.data(start_time=1, stop_time=2)

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.CONTEXT_FRAME_LIST_GET)

        world.context_frames = world.client.context_frames()

    world.first_context_frame = world.context_frames.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.CONTEXT_FRAME_OCCURRENCE_GET)

        world.cf_occurrences = world.first_context_frame.occurrences()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.EVENT_FRAME_LIST_GET)

        world.event_frames = world.client.event_frames()

    world.first_event_frame = world.event_frames.first()

    with mock.patch('requests.get') as requests_get:
        requests_get.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.EVENT_FRAME_OCCURRENCE_LIST_GET)

        world.ef_occurrences = world.first_event_frame.occurrences(1623933500000,
                                                                   1623933750000)


@step("the methods works correctly resulting in correct data types")
def step_impl(context):
    """
    Now, we assert that the variables saved in the world are of the correct data types
    """
    assert isinstance(world.client_assets, EntityList)
    for asset in world.client_assets:
        assert isinstance(asset, Asset)
    assert isinstance(world.first_asset, Asset)
    assert isinstance(world.client_asset_tags, EntityList)
    assert isinstance(world.first_asset_tags, EntityList)
    assert isinstance(world.first_tag, Tag)
    assert isinstance(world.assets_excluding_first, EntityList)
    for asset in world.assets_excluding_first:
        assert isinstance(asset, Asset)
    assert isinstance(world.assets_filtered, EntityList)
    for asset in world.assets_filtered:
        assert isinstance(asset, Asset)
    assert isinstance(world.first_asset_batches, EntityList)
    assert isinstance(world.first_asset_batches.first(), Batch)
    with mock.patch('requests.post') as requests_post:
        requests_post.return_value = TestHelpers.APIHelperCallAPI(
            TestHelpers.TAG_DATA_POST)
        assert isinstance(world.first_tag_data.index, Int64Index)
    assert isinstance(world.context_frames, EntityList)
    assert isinstance(world.first_context_frame, ContextFrame)
    assert isinstance(world.cf_occurrences, EntityList)
    assert isinstance(world.cf_occurrences.first(), ContextFrameOccurrence)
    assert isinstance(world.event_frames, EntityList)
    assert isinstance(world.first_event_frame, EventFrame)
    assert isinstance(world.ef_occurrences.first(), EventFrameOccurrence)
