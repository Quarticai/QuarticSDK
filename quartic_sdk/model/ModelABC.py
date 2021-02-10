import abc
import logging
from pprint import pprint

import sys
from typing import List

import pandas as pd
from requests import Response

from quartic_sdk.api_client import APIClient
from quartic_sdk.model.helpers import Validations, ModelUtils
from quartic_sdk.utilities.constants import MAX_MODEL_SIZE, SAVE_MODEL_ENDPOINT


class ModelABC(metaclass=abc.ABCMeta):
    """
    A Base Class Model for Wrapping User Models into Quartic Deployments.
    User need to Inherit this class and override the predict method with all the post model training steps like,
    preprocessing, prediction, postprocessing the pandas dataframe passed to :func: `predict` during real time
    prediction.

    Note: Please do not overwrite method :func: `save` as it contains utilities to validate and deploy model to Quartic

    Parameters
    ----------
    name : Name of the model to be saved in Quartic
    description : Description of the current model
    log_level : Log Level for logs created/executed during run time i.e. during real time predictions

    Attributes
    ----------
    name : Name of the model to be saved in Quartic
    description : description of model
    log_level : Log level
    log : Logger instance which can be used to set run time logs ex: self.log.info("Example Log")

    Methods
    -------
    save    :   private save method to save deploy model to quartic
    predict :   abstract predict method which needs to overridden

    Examples
    --------
    class MyModel(ModelABC):
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
                                prediction output in agreement with Quartic Platform
        :param ml_node:         Optional - Ml Node Id if deployment of model needs to be done to specific node
        :return:                None on successfully storing the model to Quartic Platform
        """
        assert isinstance(client, APIClient)
        Validations.validate_model(self, test_df)
        model_pkl = ModelUtils.get_pickled_model(self)
        assert sys.getsizeof(model_pkl) <= MAX_MODEL_SIZE

        # Need to implement rest api call part to trigger api
        request_body = {
            "model": model_pkl,
            "model_name": self.name,
            "output_tag_name": output_tag_name,
            "feature_tags": feature_tags,
            "target_tag_id": target_tag,
        }
        if ml_node:
            request_body['ml_node_id'] = ml_node

        print(request_body)
        response: Response = client.api_helper.call_api(SAVE_MODEL_ENDPOINT, method_type='POST', body=request_body)
        response.raise_for_status()

    @abc.abstractmethod
    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        """
        Abstract method for custom predict method
        :param input_df: Input Data frame for prediction
        :return:    Returns pd
        """
        pass
