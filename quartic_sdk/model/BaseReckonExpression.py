import abc
import logging
import sys
from typing import List

import pandas as pd
from requests import HTTPError

from quartic_sdk.model.helpers import ModelUtils, Validation
from quartic_sdk.utilities import constants
from functools import wraps
from quartic_sdk.utilities.exceptions import InvalidWindowDuration,MovingWindowException
from quartic_sdk.utilities.jupyter_utils import get_ipynb_name

class BaseReckonExpression(metaclass=abc.ABCMeta):
    """
    A Base Class Model for Wrapping User Models into Quartic Deployments.
    User needs to inherit this class and override the evaluate method with his operations

    Note: Please do not overwrite method :func: `save` as it contains utilities to validate and deploy expression to the Quartic AI Platform

    Methods
    -------
    save    :   private save method to save expression to the Quartic AI Platform
    predict :   abstract predict method which needs to overridden

  """

    def __init__(self, log_level: str = 'INFO'):

        self.log_level = log_level
        self.log = logging.getLogger(__name__)
        self.log.setLevel(log_level)
        self.__window_support = False
        self.__window_duration = None

    def save(self, client, output_tag_name: str,
             needs: List[int], asset: int, is_streaming: bool,
               tag_category: str, test_df: pd.DataFrame, update: bool = False):
        """

        :param client:          Quartic GraphQLClient
        :param output_tag_name: name for Expression output tag
        :param needs:    Feature Tag ids used in the model
        :param asset:     Asset Id
        :param is_streaming:    Streaming
        :param tag_category:    Tag Category
        :param test_df:         Test input dataframe to validate input and
                                prediction output in agreement with Quartic AI Platform
        :param update:          Optional - Update the model if already exists
        :return:                None on successfully storing the model to the Quartic AI Platform
        """
        from quartic_sdk import GraphqlClient
        assert isinstance(client, GraphqlClient)
        try:
            graphQLQueryGetModel = """
                query MyQuery($asset: ID!, $name: String!) {
                    TagExpression(asset: $asset, tag_ShortName_Iexact: $name) {
                        id
                    }
                }
            """
            get_result = client.execute_query(graphQLQueryGetModel, {"asset": asset, "name": output_tag_name})
            if get_result['data']['TagExpression'] and get_result['data']['TagExpression'][0]['id']:
                self.log.warning(f"Model with name {output_tag_name} with TagExpression id {get_result['data']['TagExpression'][0]['id']} already exists.")
                if not update:
                    self.log.exception("To update the model, please add argument update=True when calling the save method")
                    return
                else:
                    self.log.info("Updating the model")
                
        except HTTPError as ex:
            raise Exception(f"Failed while trying to check if model already exists: {ex.response.content.decode()}")
        except Exception as ex:
            self.log.warning(f"Failed while trying to check if model already exists: {ex}")


        test_df = ModelUtils.get_performance_test_df(test_df)
        Validation.validate_expression(self, test_df)
        model_pkl = ModelUtils.get_pickled_object(self)
        
        assert sys.getsizeof(model_pkl) <= constants.MAX_MODEL_SIZE, \
            f"model can't be more than {constants.MAX_MODEL_SIZE}MB"

        variables = {
            constants.MODEL: model_pkl,
            constants.NAME: output_tag_name,
            constants.NEEDS: needs,
            constants.ASSET: asset,
            constants.IS_STREAMING: is_streaming,
            constants.TAG_CATEGORY: tag_category,
            constants.SOURCE: "A_2",
            constants.FILE_NAME: get_ipynb_name()
        }

        graphQLQuery = """

            mutation MyMutation($asset: ID!, $model: String!, $isStreaming: Boolean!, $needs: [String]!, $name: String!, $tagCategory: Int!,
              $source: TagExpressionSourceEnumCreate!,
              $fileName: String!) {
                __typename
                TagexpressionCreate(newTagexpression: {asset: $asset, model: $model,isStreaming: $isStreaming, needs: $needs, name: $name, tagCategory: $tagCategory, source: $source, fileName: $fileName}) {
                    ok
                    errors {
                    field
                    messages
                    }
                    tagexpression {
                    id
                    isStreaming
                    }
                }
            }
        """
        
        try:
            res = client.execute_query(graphQLQuery, variables)
            self.log.info(res)
            if not res['data']['TagexpressionCreate']['ok']:
                raise Exception(res['data']['TagexpressionCreate']['errors'])
            self.log.info("Successfully saved the model to Quartic Platform")
        except HTTPError as ex:
            raise Exception(f"Failed to Save model: {ex.response.content.decode()}")

    @abc.abstractmethod
    def evaluate(self, input_df: pd.DataFrame) -> pd.Series:
        """
        Abstract method for custom predict method
        :param input_df: Input Data frame for prediction
        :return:    Returns pd
        """
        pass
    
    def with_window(duration):
        """
        This is decorator method for window support
        User can decorate predict method with this decorator for window support
        :param duration: window duration in sec
        :return:    None
        """
        def inner_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self = args[0]
                if not isinstance(duration, int):
                    raise InvalidWindowDuration(
                        'Invalid duration value passed for @BaseQuarticModel.with_window decorator'
                        )
                self.__window_support = True
                self.__window_duration = duration
                self.log.info(f"window support enabled for model with duration: {duration}")
                return func(*args, **kwargs)
            return wrapper
        return inner_decorator
    
    def moving_window_evaluate(self, input_df: pd.DataFrame, previous_df: pd.DataFrame):
        """
        This method calls predict for with window model along with respective window data for each row in input_df.
        :param input_df: input dataframe
        :param previous_df: previous dataframe for with window model
        :return: pandas series of predictions along with timestamps respective to input_df records
        """
        if input_df.empty:
            raise MovingWindowException("input_df must not be empty")
        window_df = pd.concat([previous_df, input_df])
        if not hasattr(self.evaluate,'__wrapped__'):
            raise MovingWindowException("only callable for models with window support")
        if not self.__window_duration:
            raise MovingWindowException("Predict must be called atleast once before calling moving window predict")
       
        return self.evaluate.__wrapped__(self, window_df)
