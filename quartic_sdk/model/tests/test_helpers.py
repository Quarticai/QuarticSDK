import sys
from unittest import TestCase
import pandas as pd

from quartic_sdk.utilities.exceptions import InvalidPredictionException
from quartic_sdk.model.helpers import Validations
from quartic_sdk.model.tests import ModelThatReturnsString, SlowModel


class TestModelValidations(TestCase):

    def test_validate_prediction_output(self):
        with self.assertRaises(InvalidPredictionException):
            Validations.validate_prediction_output("test output")
            Validations.validate_prediction_output(pd.Series())
            Validations.validate_prediction_output(pd.Series([None, None]))
            Validations.validate_prediction_output(pd.Series(["A", "B"]))
            Validations.validate_prediction_output(pd.Series([False, True]))
            Validations.validate_prediction_output(pd.Series([1, "A", True]))
        Validations.validate_prediction_output(pd.Series([1, 2]))
        Validations.validate_prediction_output(pd.Series([1, 2.0]))
        Validations.validate_prediction_output(pd.Series([sys.float_info.min,
                                                        sys.float_info.max, 1, 2]))

    def test_validate_model(self):
        with self.assertRaises(InvalidPredictionException):
            data = {'col_A': [1, 2], 'col_B': [3, 4]}
            Validations.validate_model(ModelThatReturnsString(), pd.DataFrame(data=data))

        with self.assertRaises(AssertionError):
            data = {'col_A': [1, 2], 'col_B': [3, 4]}
            Validations.validate_model(SlowModel(), pd.DataFrame(data=data))

    
