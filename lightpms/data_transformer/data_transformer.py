from abc import ABC, abstractmethod


class DataTransformer(ABC):
    """
    Extract data from source.
    """

    @abstractmethod
    def transform():
        pass

    @abstractmethod
    def validate_datapoint():
        pass
