from requests import HTTPError
import quartic_sdk.utilities.constants as Constants
import datetime, pytz
from pytz import timezone
from datetime import datetime


class Rule:
    """
    This helper class is used for creating and validating raw_json needed for creation of
    RuleDefinition schema for Procedure/ProcedureStep
    """
    # raw_json key types used for creating rule
    TAG = '0'
    OPERATOR = '1'

    def __init__(self, client, name, first_tag, operator, second_tag, duration_ms):
        """
        Rule class constructor
        :param client: client which is used for calling API
        :param name: Rule Name
        :param first_tag: Tag(Tag Entity) Object
        :param operator: Operator used for creating rule condition like '0' for PLUS, '1' for MINUS and so on
        :param second_tag: Tag(Tag Entity) Object
        :param duration_ms: Duration of rule in milliseconds
        """
        self.client = client
        self.name = name
        self.first_tag = first_tag
        self.operator = operator
        self.second_tag = second_tag
        self.duration_ms = duration_ms

    def raw_json(self):
        """
        This method returns raw_json schema required for RuleDefinition creation
        :return: Json Schema
        """
        return {
            "0": {
                self.TAG: str(self.first_tag.id)
            },
            "1": {
                self.OPERATOR: self.operator
            },
            "2": {
                self.TAG: str(self.second_tag.id)
            }
        }

    def rule_schema(self):
        """
        This method returns schema required for RuleDefinition creation
        :return: Json Schema
        """
        return {
            "name": self.name,
            "raw_json": self.raw_json(),
            "duration_ms": self.duration_ms,
            "tags": [self.first_tag.id, self.second_tag.id],
            "category": Constants.OTHERS
        }

    def validate_rule_raw_json(self):
        """
        This is used to validate raw_json schema
        """
        try:
            self.client.api_helper.call_api(
                Constants.POST_RULE_VALIDATE_JSON,
                method_type=Constants.API_POST,
                body={"raw_json": self.raw_json()}
            )
        except HTTPError as exception:
            raise Exception(f'Exception in validating rule: {exception.response.content.decode()}')

class TimeUtils:

    @classmethod
    def parse_telemetry_ts(cls, ts, time_zone='UTC'):
        """
        Parses as datetime.datetime, a string that represents physical
            timestamp i.e. telemetry timestamps, or the timestamps stored in
            database.
        :param ts: String/Int representing time
        :param time_zone: Timezone string
        :return: datetime.datetime with timezone. The timezone is always in UTC
            because that's how telemetry date format is designed to be.
        """
        user_tz = timezone(time_zone)
        return pytz.utc.localize(
            datetime.utcfromtimestamp(float(str(ts)) / 1000.)
        ).astimezone(user_tz)

class QueryDictConverter:
    
    @classmethod
    def convert_epoch_to_datetime(cls, query_param_dict):
        """
        Converts timestamp fields in query_params to datetime if epoch timestamp is provided.
        fields that can pass epoch timestamps are provided in set Constants.TIMESTAMPFIELDS

        :param: Dictionay representing query_params from request
        :return: Dicttionary
        """
        timestamp_fields = Constants.TIMESTAMPFIELDS
        
        for param in query_param_dict.keys():
            if param in timestamp_fields:
                try:
                    query_param_dict[param] = TimeUtils.parse_telemetry_ts(query_param_dict[param])
                except ValueError as exception:
                    """
                    support the datetime timestamps as well
                    """
                    pass                
        return query_param_dict