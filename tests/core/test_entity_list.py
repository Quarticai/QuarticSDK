
import pytest
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
from quartic_sdk.utilities.test_helpers import (
    ASSET_LIST_GET, TAG_LIST_GET, SINGLE_ASSET_GET, TAG_LIST_MULTI_GET)

asset_entity_list = EntityFactory(Constants.ASSET_ENTITY, ASSET_LIST_GET, None)
new_asset_entity_list = EntityFactory(
    Constants.ASSET_ENTITY, ASSET_LIST_GET, None)
second_asset_entity = EntityFactory(
    Constants.ASSET_ENTITY, SINGLE_ASSET_GET, None)
test_asset_entity = EntityFactory(
    Constants.ASSET_ENTITY, ASSET_LIST_GET[0], None)
test_new_asset_entity = EntityFactory(
    Constants.ASSET_ENTITY, SINGLE_ASSET_GET, None)
test_tag_entity = EntityFactory(Constants.TAG_ENTITY, TAG_LIST_GET[0], None)
test_tag_entities_list = EntityFactory(
    Constants.TAG_ENTITY, TAG_LIST_MULTI_GET, None)


def test_entity_list_validate_type():
    """
    We test the `_validate_type` method in EntityList
    """
    assert asset_entity_list._validate_type(test_asset_entity)
    assert not asset_entity_list._validate_type(test_tag_entity)


def test_entity_list_get():
    """
    Test get method of entitylist
    """
    assert asset_entity_list.get("id", 1) == test_asset_entity


def test_entity_list_all():
    """
    Test all method of entitylist
    """
    assert len(asset_entity_list.all()) == 1


def test_entity_list_count():
    """
    Test count method of entitylist
    """
    assert asset_entity_list.count() == 1


def test_entity_list_equality():
    """
    Test that the equality method of entity list is working correctly
    """
    with pytest.raises(AssertionError):
        asset_entity_list == test_asset_entity
    with pytest.raises(AssertionError):
        asset_entity_list != test_tag_entities_list
    assert asset_entity_list == new_asset_entity_list
    new_asset_entity_list.add(second_asset_entity)
    assert asset_entity_list != new_asset_entity_list


def test_entity_list_add():
    """
    Test add method of entitylist for correct and incorrect class types
    """
    added_entity_list = asset_entity_list
    added_entity_list.add(test_new_asset_entity)
    assert added_entity_list.count() == 2
    with pytest.raises(Exception):
        added_entity_list.add(test_tag_entity)


def test_entity_list_first():
    """
    Test first method of entitylist
    """
    assert asset_entity_list.first() == test_asset_entity


def test_entity_list_filter():
    """
    Test filter method of EntityList
    """
    assert test_tag_entities_list.filter(id=1).count() == 1
    assert test_tag_entities_list.filter(id__ne=1).count() == 3
    assert test_tag_entities_list.filter(tag_data_type="double").count() == 3
    assert test_tag_entities_list.filter(tag_data_type__eq="string").count() == 1
    assert test_tag_entities_list.filter(id__le=3).count() == 3
    assert test_tag_entities_list.filter(id__lt=3).count() == 2
    assert test_tag_entities_list.filter(tag_data_type="double", asset=1).count() == 2
    assert test_tag_entities_list.filter(tag_data_type="double", asset=2).count() == 1


def test_entity_list_exclude():
    """
    Test exclude method of EntityList
    """
    assert test_tag_entities_list.exclude(id=1).count() == 3
    assert test_tag_entities_list.exclude(tag_data_type="double").count() == 1
    assert test_tag_entities_list.exclude(tag_data_type="string").count() == 3
    assert test_tag_entities_list.exclude(asset=1).count() == 2
    assert test_tag_entities_list.exclude(asset=3).count() == 3
    assert test_tag_entities_list.exclude(id__gt=1).count() == 1
    assert test_tag_entities_list.exclude(id__ge=1).count() == 0
    assert test_tag_entities_list.exclude(id=1, tag_data_type="string").count() == 2
