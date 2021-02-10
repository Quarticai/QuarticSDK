import hashlib

import cloudpickle
import base64
import math
import numpy as np
import pandas as pd
from time import time

from quartic_sdk.utilities.exceptions import InvalidPredictionException
from quartic_sdk.utilities.constants import NUM_ROW_PER_PREDICTION, MAX_PREDICTION_PROCESSING_TIME


class Validations(object):
    """
    Contains Validation functions for ml models
    """
    @classmethod
    def get_performance_test_df(cls, test_df: pd.DataFrame):
        """
        Creates a Test data frame of size 100 rows(for 30sec batch approximation)
        :param test_df: Test Data frame
        :return: Returns test dataframe with configured number of rows
        """
        if test_df.shape[0] == NUM_ROW_PER_PREDICTION:
            return test_df
        elif test_df.shape[0] < NUM_ROW_PER_PREDICTION:
            current_size = test_df.shape[0]
            num_repetition = math.ceil(NUM_ROW_PER_PREDICTION / int(current_size))
            return pd.concat([test_df] * num_repetition, ignore_index=True).head(NUM_ROW_PER_PREDICTION)
        else:
            return test_df.head(NUM_ROW_PER_PREDICTION)

    @classmethod
    def get_model_prediction_and_time(cls, model, test_df):
        """
        evaluates prediction of model with test data frame
        :param model:   Instance ModelABC
        :param test_df: Test Dataframe
        :return:        tuple of prediction and processing time
        """
        start_time = time()
        prediction = model.predict(test_df)
        end_time = time()

        return prediction, end_time - start_time

    @classmethod
    def validate_prediction_output(cls, result: pd.Series):
        """
        Validates if prediction output is of type Series and values of series are float64
        :param result: pandas series
        :return:    None
        :raises:    InvalidPredictionException
        """
        if not isinstance(result, pd.Series):
            raise InvalidPredictionException("Output of model.predict should be of type pandas Series")
        if result.empty or result.isnull().all():
            raise InvalidPredictionException("Prediction result for given test data was empty or None for all the rows."
                                             " Please verify the model")
        if not np.array_equal(result.fillna(0), result.fillna(0).astype(np.float64)):
            raise InvalidPredictionException("Prediction result of type other than int/float/double are not supported")

    @classmethod
    def validate_model(cls, model, test_df):
        """
        Validates the model for size and performance
        :param model:   Instance of ModelABC
        :param test_df: Test dataframe
        """
        performance_test_df = cls.get_performance_test_df(test_df)
        prediction_result, processing_time = cls.get_model_prediction_and_time(model, performance_test_df)
        cls.validate_prediction_output(prediction_result)
        assert processing_time <= MAX_PREDICTION_PROCESSING_TIME


class ModelUtils(object):
    """
    Contains utils to pickle model and add checksum
    """

    @classmethod
    def get_checksum(cls, model_bytes):
        """
        Calculates the checksum for given byte array
        :param model_bytes: pickeled model
        :return:            Returns the checksum of model
        """
        return hashlib.md5(model_bytes).hexdigest()

    @classmethod
    def get_pickled_model(cls, model):
        """
        Generates pickle for model and adds checksum to it
        :param model:   Model to pickle
        :return:        Pickled Model as string
        """

        model_pkl = cloudpickle.dumps(model)
        model_string = base64.b64encode(model_pkl)
        checksum = cls.get_checksum(model_string)
        print(checksum)
        return checksum + model_string.decode()
