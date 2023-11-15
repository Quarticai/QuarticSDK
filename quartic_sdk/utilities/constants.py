# Authentication types
OAUTH = 1
BASIC = 2

# MODEL Constants
NUM_ROW_PER_PREDICTION = 100
MAX_PREDICTION_PROCESSING_TIME = 10  # In seconds
MAX_MODEL_SIZE = 100 * 1024 * 1024  # 100 MB
MODEL = "model"
MODEL_NAME = "model_name"
OUTPUT_TAG_NAME = "output_tag_name"
FEATURE_TAGS = "feature_tags"
TARGET_TAG_ID = "target_tag_id"
TEST_DATA = "test_data"
ML_NODE_ID = "ml_node_id"

NAME = 'name'
NEEDS = 'needs'
ASSET = 'asset'
TAG_CATEGORY = 'tagCategory'
SOURCE = 'source'
IS_STREAMING = 'isStreaming'
FILE_NAME = 'fileName'


# Model Type Integer Constants and their mapping
MODEL_TYPE_ALL = 0
MODEL_TYPE_TELEMETRY = 1
MODEL_TYPE_SPECTRAL = 2

MODEL_TYPE = {
    MODEL_TYPE_ALL: "All",
    MODEL_TYPE_TELEMETRY: "Telemetry",
    MODEL_TYPE_SPECTRAL: "Spectral"
}

# API method types
METHOD_TYPES = ["GET", "POST", "PUT", "PATCH", "DELETE"]
API_GET = "GET"
API_POST = "POST"
API_PATCH = "PATCH"
API_PUT = "PUT"
API_DELETE = "DELETE"

# API calls
GET_ASSETS = "/api/v1/asset/"
GET_CONTEXT_FRAME_DEFINITIONS = "/api/v1/context_frame_definitions/"
GET_EDGE_CONNECTORS = "/api/v1/edge_connector/"
GET_TAGS = "/api/v1/tags/"
RETURN_TAG_DATA = "/api/v1/tag_data/"
RETURN_TAG_DATA_CURSOR = "/api/v1/tag_data_cursor/"
GET_CONTEXT_FRAME_OCCURRENCES = "/api/v1/context_frame_occurrences/"
GET_BATCHES = "/api/v1/batches/"
GET_EVENT_FRAMES = "/api/v1/event_frame/"
GET_EVENT_FRAME_OCCURRENCES = "/api/v1/ef_occurrence/"
POST_OPCUA_DATA = "/api/v1/historical_tag_data/"
CMD_MODEL_ENDPOINT = '/cmd/model/'
GET_SITES = "/api/v1/site/"
GET_PRODUCTS = "/api/v1/product/"
PROCEDURES = "/api/v1/procedure/"
PROCEDURE_STEPS = "/api/v1/procedure_step/"
POST_RULE_VALIDATE_JSON = "/api/v1/rule_validate_json/"

# Entity types
ASSET_ENTITY = "Asset"
BATCH_ENTITY = "Batch"
CONTEXT_FRAME_ENTITY = "ContextFrame"
CONTEXT_FRAME_OCCURRENCE_ENTITY = "ContextFrameOccurrence"
TAG_ENTITY = "Tag"
EDGE_CONNECTOR_ENTITY = "EdgeConnector"
MODEL_ENTITY = "Model"
EVENT_FRAME_ENTITY = "EventFrame"
EVENT_FRAME_OCCURRENCE_ENTITY = "EventFrameOccurrence"
SITE_ENTITY = "Site"
PRODUCT_ENTITY = "Product"
PROCEDURE_ENTITY = "Procedure"
PROCEDURE_STEP_ENTITY = "ProcedureStep"

# Data return type constants
RETURN_JSON = "json"
RETURN_PANDAS = "pd"

# Integer Constants and their mapping with Suitable String Constants
INIT = 0
ACTIVE = 1
PARTIAL_STREAMING = 2
INACTIVE = 3
UNASSIGNED_TAGS = 4

STATUS = {
    INIT: "Initial",
    ACTIVE: "Active",
    PARTIAL_STREAMING: "Partial Streaming",
    INACTIVE: "Inactive",
    UNASSIGNED_TAGS: "Unassigned Tags"
}

ABDF1 = 200
OPTO22 = 201
OPCDA = 202
OSIPI = 203
MODBUS = 204
MQTT = 205
OPCUA = 206
SQL = 207
SPECTRAL = 208

CONNECTOR_PROTOCOLS = {
    ABDF1: 'ABDF1',
    OPTO22: 'OPTO22',
    OPCDA: 'OPCDA',
    MODBUS: 'MODBUS',
    MQTT: 'MQTT',
    OSIPI: 'OSIPI',
    OPCUA: 'OPCUA',
    SQL: 'SQL',
    SPECTRAL: 'SPECTRAL'
}

RAW_TAG = 1
SOFT_TAG = 2
AGGREGATION_TAG = 3
BITWISE_TAG = 4
WRITEBACK_TAG = 5

TAG_TYPES = {
    RAW_TAG: "Raw Tag",
    SOFT_TAG: "Soft Tag",
    AGGREGATION_TAG: "Aggregation Tag",
    BITWISE_TAG: "Bitwise Tag",
    WRITEBACK_TAG: "Writeback Tag"
}

DOUBLE = 0
STRING = 1
BOOLEAN = 2
INT = 3
LONG = 4
FLOAT = 5
SPECTRAL = 6

TAG_DATA_TYPES = {
    DOUBLE: "double",
    STRING: "string",
    BOOLEAN: "boolean",
    INT: "int",
    LONG: "long",
    FLOAT: "float",
    SPECTRAL: "spectral"
}

CAT = 0
CONTI = 1

TAG_VALUE_TYPES = {
    CAT: "Discrete",
    CONTI: "Continuous"
}

PROCESS_VARIABLE = 1
CONDITION_VARIABLE = 2
PROCESS_ALARM = 3
PROCESS_EVENT = 4
ANOMALY_SCORE = 5
PREDICTED_VARIABLE = 6
OTHERS = 7
WORKFLOW = 8
INFLUENCING_SCORE = 9

PROCESS_VARIABLE_TYPES = {
    PROCESS_VARIABLE: 'Process Variable',
    PROCESS_ALARM: 'Process Alarm',
    PROCESS_EVENT: 'Process Event',
    CONDITION_VARIABLE: 'Condition Variable',
    ANOMALY_SCORE: 'Anomaly Score',
    PREDICTED_VARIABLE: 'Predicted Variable',
    WORKFLOW: 'Workflow',
    OTHERS: 'Others',
    INFLUENCING_SCORE: 'Influencing Score',
}

ENERGY = 1
THROUGHPUT = 2
RELIABILITY = 3
QUALITY = 4
SAFETY = 5
ENVIRONMENT = 6
OTHERS = 7

INTELLIGENCE_CATEGORIES = {
    ENERGY: 'Energy',
    THROUGHPUT: 'Throughput',
    RELIABILITY: 'Reliability',
    QUALITY: 'Quality',
    SAFETY: 'Safety',
    ENVIRONMENT: 'Environment',
    OTHERS: 'Others'
}

DEFAULT_PAGE_LIMIT_ROWS = 200000
DEFAULT_BATCH_SIZE = 200000

# Operators needed for creating raw_json for rules creation
PLUS = '0'
MINUS = '1'
MULTIPLY = '3'
DIVIDE = '4'
EXPONENT = '5'
LESSER = '6'
GREATER = '7'
LESSER_EQUAL = '8'
GREATER_EQUAL = '9'
EQUAL = '10'
RANGE = '11'
AND = '12'
OR = '13'

MAX_BATCH_SIZE_FOR_PAGINATED_QUERY = 20_000
