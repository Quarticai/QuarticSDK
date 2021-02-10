

class InvalidPredictionException(Exception):
    """
    Base Exception for Prediction Output Validation
    """
    def __init__(self, message):
        super().__init__(message)


class ModelSaveException(Exception):
    """
    Exception that occurs during save model api
    """
    def __init__(self, message):
        def __init__(self, message):
            super().__init__(message)