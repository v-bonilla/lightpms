from abc import ABC, abstractmethod


class DataLoader(ABC):
    """
    Extract data from source.
    """

    @abstractmethod
    def load():
        pass
