import logging
from typing import Any, Generator, List

from lightpms.dao.daos import TransactionDAO
from lightpms.data_loader.data_loader import DataLoader
from lightpms.model.models import Transaction

logger = logging.getLogger(__name__)


class TransactionLoader(DataLoader):
    def __init__(self, transaction_dao: TransactionDAO) -> None:
        super().__init__()
        self._transaction_dao = transaction_dao

    def load(self, transactions: Generator[Transaction, Any, None]) -> None:
        logger.debug(f"Loading transactions into database")
        self._transaction_dao.insert_transactions(transactions)
