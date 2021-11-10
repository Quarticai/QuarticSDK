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


class BaseQuarticModel(metaclass=abc.ABCMeta):
    """
    A Base Class Model for Wrapping User Models into Quartic Deployments.
    User needs to inherit this class and override the predict method with all the post model training steps such as,
    preprocessing, prediction, postprocessing the pandas dataframe passed to :func: `predict` during real time
    prediction.

    Note: Please do not overwrite method :func: `save` as it contains utilities to validate and deploy model to the Quartic AI Platform

    Parameters
    ----------
    name : Name of the model to be saved in Quartic AI Platform
    description : Description of the current model
    log_level : Log Level for logs created/executed during run time i.e. during real time predictions

    Attributes
    ----------
    name : Name of the model to be saved in Quartic AI Platform
    description : description of model
    log_level : Log level
    log : Logger instance which can be used to set run time logs ex: self.log.info("Example Log")

    Methods
    -------
    save    :   private save method to save deploy model to the Quartic AI Platform
    predict :   abstract predict method which needs to overridden

    Examples
    --------
    class MyModel(BaseQuarticModel):
        def __init__(self, model):
            self.model = model
            super().__init__('MyModel', 'model description', 'INFO')

        def preprocess(self, input_df):
            transformed_df = custom_transform(input_df)
            return transformed_df

        def postprocess(self, input_df):
            transformed_df = custom_transform_post(input_df)
            return transformed_df

        def predict(self, input_df):
            pre_transformed_df = self.preprocess(input_df)
            prediction_df = self.model.predict(pre_transformed_df)
            self.log.info("Test Log")
            return postprocess(prediction_df)['output_column'] # pandas Series

    lr = LinearRegression()
    lr.train(input_data)
    my_model = MyModel(lr)
    my_model.save('my_model_output', [Tag('A'), Tag('B')], Tag('C'), input_data, None)
    """

    def __init__(self, name: str, description: str = '', log_level: str = 'INFO'):
        self.name = name
        self.description = description
        self.log_level = log_level
        self.log = logging.getLogger(name)
        self.log.setLevel(log_level)
        self.__window_support = False
        self.__window_duration = None

    def save(self, client, output_tag_name: str,
             feature_tags: List[int],
             target_tag: int,
             test_df: pd.DataFrame,
             ml_node: int = None):
        """

        :param client:          Quartic APIClient
        :param output_tag_name: name for Prediction output tag
        :param feature_tags:    Feature Tag ids used in the model
        :param target_tag:      Target tag id to specify the parent of current soft tag
        :param test_df:         Test input dataframe to validate input and
                                prediction output in agreement with Quartic AI Platform
        :param ml_node:         Optional - Ml Node Id if deployment of model needs to be done to specific node
        :return:                None on successfully storing the model to the Quartic AI Platform
        """
        from quartic_sdk import APIClient
        assert isinstance(client, APIClient)
        test_df = ModelUtils.get_performance_test_df(test_df)
        test_data = ModelUtils.get_pickled_object(test_df.head(5))
        model_pkl = ModelUtils.get_pickled_object(self)
        Validation.validate_model(self, test_df)
        assert sys.getsizeof(model_pkl) <= constants.MAX_MODEL_SIZE, \
            f"model can't be more than {constants.MAX_MODEL_SIZE}MB"

        # Need to implement rest api call part to trigger api
        request_body = {
            constants.MODEL: model_pkl,
            constants.MODEL_NAME: self.name,
            constants.OUTPUT_TAG_NAME: output_tag_name,
            constants.FEATURE_TAGS: feature_tags,
            constants.TARGET_TAG_ID: target_tag,
            constants.TEST_DATA: test_data
        }
        if ml_node:
            request_body[constants.ML_NODE_ID] = ml_node
        try:
            client.api_helper.call_api(constants.CMD_MODEL_ENDPOINT,
                                       method_type=constants.API_POST,
                                       body=request_body)
            self.log.info("Successfully saved the model to Quartic Platform")
        except HTTPError as ex:
            raise Exception(f"Failed to Save model: {ex.response.content.decode()}")

    @abc.abstractmethod
    def predict(self, input_df: pd.DataFrame) -> pd.Series:
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
    
    def moving_window_predict(self, input_df: pd.DataFrame, previous_df: pd.DataFrame):
        """
        This method calls predict for with window model along with respective window data for each row in input_df.
        :param input_df: input dataframe
        :param previous_df: previous dataframe for with window model
        :return: pandas series of predictions along with timestamps respective to input_df records
        """
        if input_df.empty:
            raise MovingWindowException("input_df must not be empty")
        window_df = pd.concat([previous_df, input_df])
        predictions = pd.Series()
        if not hasattr(self.predict,'__wrapped__'):
            raise MovingWindowException("only callable for models with window support")
        if not self.__window_duration:
            raise MovingWindowException("Predict must be called atleast once before calling moving window predict")
       
        for index, row in input_df.iterrows():
            start_ts = int(index) - self.__window_duration * 1000
            df_to_predict = window_df.loc[(window_df.index >= start_ts) & (window_df.index <= int(index))]
            prediction = self.predict.__wrapped__(self, df_to_predict)
            if prediction:
                predictions.loc[index] = prediction

        
        return predictions
