import sys
from unittest import TestCase
import pandas as pd
import numpy as np
from quartic_sdk.exceptions import InvalidPredictionException
from quartic_sdk.model.helpers import ModelUtils, Validation
from quartic_sdk.model.tests import ModelThatReturnsString, SlowModel, SpectralModelThatReturnsString, SlowSpectralModel


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

    def test_validate_model(self):
        with self.assertRaises(InvalidPredictionException):
            data = {'col_A': [1, 2], 'col_B': [3, 4]}
            Validation.validate_model(ModelThatReturnsString(), pd.DataFrame(data=data))

        with self.assertRaises(InvalidPredictionException):
            data = {'col_A': [1, 2], 'col_B': [3, 4]}
            Validation.validate_model(SlowModel(), pd.DataFrame(data=data))

    def test_validate_spectral_model(self):
        with self.assertRaises(InvalidPredictionException):
            data = {'wavenum_1': ['1460000.0','1460001.0'], 'wavenum_2': ['1490004.0','1490005.0']}
            Validation.validate_model(SpectralModelThatReturnsString(), pd.DataFrame(data=data))   

        with self.assertRaises(InvalidPredictionException):
            data = {'wavenum_1': ['1460000.0','1460001.0'], 'wavenum_2': ['1490004.0','1490005.0']}
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
