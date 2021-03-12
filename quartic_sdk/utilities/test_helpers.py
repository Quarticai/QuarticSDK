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


# Test constants
ASSET_LIST_GET = [{"id": 1, "name": "Asset_name", "edge_connectors": [1, 2]}]
TAG_LIST_GET = [{"id": 1, "name": "Tag1", "short_name": "Short Tag1", "edge_connector": 1, "asset": 1}]
TAG_DATA_POST = {"columns": [1], "index": [12121212,12121222,12121232], "data": [[2], [3], [4]], "count": 1, "offset": 0}
ASSET_DATA_POST = {"columns": [1, 2, 3], "index": [12121212,12121222,12121232], "data": [[2, 3, 1], [3, 1, 2], [4, 1, 2]], "count": 3, "offset": 0}
SINGLE_ASSET_GET = {"id": 2, "name": "Asset_name2", "edge_connectors": [1, 2]}
TAG_LIST_MULTI_GET = [{"id": 1, "name": "Tag1", "short_name": "Short Tag1", "edge_connector": 1, "asset": 1},
    {"id": 2, "name": "Tag2", "short_name": "Short Tag2", "edge_connector": 1, "asset": 1}]
TAG_LIST_DATA_POST = {"columns": [1, 2], "index": [1,2], "data": [[1, 2], [2,3]], "count": 3, "offset": 0}
BATCH_LIST_GET = [{"id": 1, "name": 12121212, "start": 1212, "stop": 2121}]
CONTEXT_FRAME_LIST_GET = [{"id": 1, "name": "CFD1", "description": "CFD description", "pu_or_wc": "PU"}]
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
EDGE_CONNECTOR_LIST_GET = [{"id": 1, "name": "Edge connector name", "connector_protocol": 201}]
EDGE_CONNECTOR_DATA_POST = {"columns": [1, 2, 3], "index": [1,2,3], "data": [[2, 3, 1], [3, 1, 2], [4, 1, 2]], "count": 3, "offset": 0}

