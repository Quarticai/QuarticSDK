from unittest.mock import Mock
import pandas as pd
import time

from quartic_sdk.model.ModelABC import ModelABC
from quartic_sdk.utilities import constants


class SupportedModel(ModelABC):
    def __init__(self):
        super().__init__("test_model")

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return input_df['col_A']


class ModelThatReturnsString(ModelABC):
    def __init__(self):
        super().__init__("test_model")

    def pre_transform(self, df):
        df['col_A'] = df['col_A'].astype(str)
        return df

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return self.pre_transform(input_df)['col_A']


class SlowModel(ModelABC):
    def __init__(self):
        super().__init__("test_model")

    def pre_transform(self, df):
        time.sleep(constants.MAX_PREDICTION_PROCESSING_TIME+1)
        return df

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return self.pre_transform(input_df)['col_A']
