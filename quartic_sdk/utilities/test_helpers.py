class APIHelperCallAPI:
    """
    The class is used to mock the call API which in turn calls the `requests`
    get, post, patch, put and delete methods
    """

    def __init__(self, body_json):
        """
        We initialize the class
        """
        self._json = body_json

    def json(self):
        """
        The method is called in the actual implementation to get the json
        form of the response object
        """
        return self._json

    def raise_for_status(self):
        return None
    
    @property
    def status_code(self):
        return 200


# Test constants
ASSET_LIST_GET = [{"id": 1, "name": "Asset_name", "edge_connectors": [1, 2]}]
TAG_LIST_GET = [{"id": 1,
                 "name": "Tag1",
                 "short_name": "Short Tag1",
                 "edge_connector": 1,
                 "asset": 1,
                 "tag_data_type": 0}]
TAG_DATA_POST = {
    "data": {
        "columns": ["1"], "index": [
            12121212, 12121222, 12121232], "data": [
                [2], [3], [4]]}, "total_count": {
                    "1": 3}, "page_count": {
                        "1": 3}, "cursor": None}
ASSET_DATA_POST = {
    "data": {
        "columns": [
            "1", "2", "3"], "index": [
                12121212, 12121222, 12121232], "data": [
                    [
                        2, 3, 1], [
                            3, 1, 2], [
                                4, 1, 2]]}, "total_count": {
                                    "1": 3, "2": 3, "3": 3}, "page_count": {
                                        "1": 3, "2": 3, "3": 3}, "cursor": None}
SINGLE_ASSET_GET = {"id": 2, "name": "Asset_name2", "edge_connectors": [1, 2]}
TAG_LIST_MULTI_GET = [{"id": 1,
                       "name": "Tag1",
                       "short_name": "Short Tag1",
                       "edge_connector": 1,
                       "asset": 1,
                       "tag_data_type": 0},
                      {"id": 2,
                       "name": "Tag2",
                       "short_name": "Short Tag2",
                       "edge_connector": 1,
                       "asset": 1,
                       "tag_data_type": 0},
                      {"id": 3,
                       "name": "Tag3",
                       "short_name": "Short Tag3",
                       "edge_connector": 1,
                       "asset": 2,
                       "tag_data_type": 0
                       },
                      {"id": 4,
                       "name": "Tag4",
                       "short_name": "Short Tag4",
                       "edge_connector": 2,
                       "asset": 3,
                       "tag_data_type": 1
                       }
                      ]
TAG_LIST_DATA_POST = {
    "data": {
        "columns": [
            "1", "2"], "index": [
                1, 2], "data": [
                    [
                        1, 2], [
                            2, 3]]}, "total_count": {
                                "1": 2, "2": 2}, "page_count": {
                                    "1": 2, "2": 2}, "cursor": None}
BATCH_LIST_GET = [{"id": 1, "name": 12121212, "start": 1212, "stop": 2121}]
CONTEXT_FRAME_LIST_GET = [{"id": 1, "name": "CFD1",
                           "description": "CFD description", "pu_or_wc": "PU"}]
CONTEXT_FRAME_OCCURRENCE_GET = [
    {
        "id": 1,
        "start_ef_occurrence": {
            "start_time": 12121212,
            "stop_time": 21212121
        },
        "stop_ef_occurrence": {
            "start_time": 12121212,
            "stop_time": 21322132
        },
        "sub_context_frame_occurrences": [
            {
                "event_frame_id": 2,
                "start_time": 2000000,
                "stop_time": 2100000
            }
        ],
        "context_frame": 1,
        "is_valid": True
    }
]
EDGE_CONNECTOR_LIST_GET = [{"id": 1,
                            "name": "Edge connector name",
                            "connector_protocol": 201}]
EDGE_CONNECTOR_DATA_POST = {
    "data": {
        "columns": [
            "1", "2", "3"], "index": [
                1, 2, 3], "data": [
                    [
                        2, 3, 1], [
                            3, 1, 2], [
                                4, 1, 2]]}, "total_count": {
                                    "1": 3, "2": 3, "3": 3}, "page_count": {
                                        "1": 3, "2": 3, "3": 3}, "cursor": None}

EVENT_FRAME_LIST_GET = [
    {
        "id": 1,
        "stop_rule_json": {
            "xp1": {
                "v1": "tag1624",
                "v2": "12.0",
                "opr": "<"
            }
        },
        "start_rule_json": {
            "xp1": {
                "v1": "tag1624",
                "v2": "4.0",
                "opr": ">"
            }
        },
        "start_raw_json": {
            "0": {
                "0": "1624"
            },
            "1": {
                "1": "7"
            },
            "2": {
                "2": "4.0"
            }
        },
        "stop_raw_json": {
            "0": {
                "0": "1624"
            },
            "1": {
                "1": "6"
            },
            "2": {
                "2": "12.0"
            }
        },
        "created_at": "2020-11-19T09:21:07.536136Z",
        "updated_at": "2020-11-19T09:21:07.536177Z",
        "name": "stop_ef",
        "start_duration_ms": 1000,
        "stop_duration_ms": 1000,
        "category": 3,
        "asset_permission": 51,
        "asset": 51,
        "created_by": 1,
        "tags": []
    }
]

EVENT_FRAME_OCCURRENCE_LIST_GET = [
    {'id': 460803,
     'name': 'testef',
     'start_time': 1623933598133,
     'stop_time': 1623933598134,
     'event_frame_definition': 22,
     'tags': [7735, 7739, 7751],
     'parent_tags': []
     }
]

JWT_TOKEN_RESPONSE = {
    "access": "test-access",
    "refresh": "test-refresh"
}
