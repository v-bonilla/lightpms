from abc import ABC, abstractmethod


class DataExtractor(ABC):
    """
    Extract data from source.
    """

    @abstractmethod
    def extract():
        pass
