from abc import ABC, abstractmethod


class ETL(ABC):
    """
    Runs a process to extract, transform and load data.
    """

    @abstractmethod
    def run():
        pass
