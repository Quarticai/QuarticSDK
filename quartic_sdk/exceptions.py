

class InvalidPredictionException(Exception):
    """
    Base Exception for Prediction Output Validation
    """
    def __init__(self, message):
        super().__init__(message)

class InvalidValueException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)