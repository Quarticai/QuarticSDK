# Authentication types
OAUTH = 1
BASIC = 2

NUM_ROW_PER_PREDICTION = 100
MAX_PREDICTION_PROCESSING_TIME = 10  # In seconds
MAX_MODEL_SIZE = 100 * 1024 * 1024  # 100 MB

# API method types
METHOD_TYPES = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# API calls
GET_ASSETS = "/api/v1/asset/"
GET_CONTEXT_FRAME_DEFINITIONS = "/api/v1/context_frame_definitions/"
GET_TAGS = "/api/v1/tags/"
POST_TAG_DATA = "/api/v1/tag_data/"
GET_CONTEXT_FRAME_OCCURRENCES = "/api/v1/context_frame_occurrences/"
GET_BATCHES = "/api/v1/batches/"
SAVE_MODEL_ENDPOINT = '/cmd/model/'
LIST_MODELS_ENDPOINT = '/cmd/models'
GET_MODEL_ENDPOINT = '/cmd/model/'
