import sys
from unittest import TestCase
from unittest.mock import patch
import pandas as pd
import numpy as np
from quartic_sdk.exceptions import InvalidPredictionException
from quartic_sdk.utilities.exceptions import InvalidWindowDuration,MovingWindowException
from quartic_sdk.model.helpers import ModelUtils, Validation
from quartic_sdk.model.tests import SpectralModelThatReturnsString, SlowSpectralModel
from quartic_sdk.utilities import constants


class TestModelValidations(TestCase):

    def test_validate_prediction_output(self):
        with self.assertRaises(InvalidPredictionException):
            Validation.validate_prediction_output("test output")
            Validation.validate_prediction_output(pd.Series())
            Validation.validate_prediction_output(pd.Series([None, None]))
            Validation.validate_prediction_output(pd.Series(["A", "B"]))
            Validation.validate_prediction_output(pd.Series([False, True]))
            Validation.validate_prediction_output(pd.Series([1, "A", True]))
        Validation.validate_prediction_output(pd.Series([1, 2]))
        Validation.validate_prediction_output(pd.Series([1, 2.0]))
        Validation.validate_prediction_output(pd.Series([sys.float_info.min,
                                                         sys.float_info.max, 1, 2]))

                  

    def test_validate_spectral_model(self):
        with self.assertRaises(InvalidPredictionException):
            data = {'wavenum_1': ['1460000.0','1460001.0'], 'wavenum_2': ['1490004.0','1490005.0']}
            Validation.validate_model(SpectralModelThatReturnsString(), pd.DataFrame(data=data))   
        
        with patch.object(Validation,"get_model_prediction_and_time") as MockPredictionAndTiming:
            data = {'wavenum_1': ['1460000.0','1460001.0'], 'wavenum_2': ['1490004.0','1490005.0']}
            prediction = pd.Series([i for i in range(pd.DataFrame(data=data).shape[0])])
            MockPredictionAndTiming.return_value = prediction , constants.MAX_PREDICTION_PROCESSING_TIME + 1
            
            with self.assertRaises(InvalidPredictionException):
                Validation.validate_model(SlowSpectralModel(), pd.DataFrame(data=data))        

    def test_pickle_model(self):
        model_byte_array = ModelUtils.get_pickled_object("test model object")
        checksum_data = model_byte_array[:32]
        recalculated_checksum = ModelUtils.get_checksum(model_byte_array[32:].encode())
        self.assertEqual(checksum_data, recalculated_checksum)

    def test_get_performance_test_df(self):
        df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))
        self.assertTrue(df.equals(ModelUtils.get_performance_test_df(df)))

        df = pd.DataFrame(np.random.randint(0, 1000, size=(1000, 4)), columns=list('ABCD'))
        self.assertTrue(df.head(100).equals(ModelUtils.get_performance_test_df(df)))

        df = pd.DataFrame(np.random.randint(0, 50, size=(50, 4)), columns=list('ABCD'))
        self.assertTrue(df.equals(ModelUtils.get_performance_test_df(df).head(50)))
        self.assertTrue(df.equals(
            ModelUtils.get_performance_test_df(df).tail(50).reset_index().drop('index', axis=1)))
