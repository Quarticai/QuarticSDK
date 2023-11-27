import logging

import pandas as pd
import time
from quartic_sdk.core.entities.base import Base

from quartic_sdk.utilities import constants
from quartic_sdk.model import BaseSpectralModel



class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }


class SupportedSpectralModel(BaseSpectralModel):
    """
    Example Model used for testing spectral model
    This is a valid spectral model that can be saved to the Quartic AI Platform
    """
    def __init__(self):
        super().__init__("test_spectral_model")

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        return pd.Series([i for i in range(input_df.shape[0])])

class SpectralModelThatReturnsString(BaseSpectralModel):
    """
    Example Model used for testing spectral model
    This is a invalid spectral model whose predict function returns data of type string
    """

    def __init__(self):
        super().__init__("test_spectral_model")

    def post_transform(self, data):
        data = data.astype(str)
        return data

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        output = pd.Series([i for i in range(input_df.shape[0])])
        return self.post_transform(output)

class SlowSpectralModel(BaseSpectralModel):
    """
    Example Model used for testing spectral model
    This is a invalid spectral model whose predict function takes longer processing time than that is supported by the Quartic AI Platform
    """

    def __init__(self):
        super().__init__("test_spectral_model")

    def pre_transform(self, df):
        """
        A simple transformation that sleeps for x secs before returning same
        """
        time.sleep(constants.MAX_PREDICTION_PROCESSING_TIME + 1)
        return df

    def predict(self, input_df: pd.DataFrame) -> pd.Series:
        """
            sample prediction
        """
        self.pre_transform(input_df)
        return pd.Series([i for i in range(input_df.shape[0])])
