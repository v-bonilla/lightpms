import datetime
import logging

from lightpms.dao.daos import TransactionDAO
from lightpms.data_extractor.transaction_extractor import TransactionExtractor
from lightpms.data_loader.transaction_loader import TransactionLoader
from lightpms.data_transformer.transaction_transformer import TransactionTransformer
from lightpms.etl.etl import ETL

logger = logging.getLogger(__name__)


class TransactionETL(ETL):
    """Runs the ETL for transactions."""

    def __init__(
        self,
        transaction_dao: TransactionDAO,
        transaction_extractor: TransactionExtractor,
        transaction_transformer: TransactionTransformer,
        transaction_loader: TransactionLoader,
    ) -> None:
        self._transaction_dao = transaction_dao
        self._transaction_extractor = transaction_extractor
        self._transaction_transformer = transaction_transformer
        self._transaction_loader = transaction_loader

    def run(self, start_dt: datetime.datetime, end_dt: datetime.datetime):
        """Runs the ETL for transactions."""
        logger.info(f"Running transaction ETL from {start_dt} to {end_dt}")
        logger.debug(
            f"Extracting transactions from data source between {start_dt} and {end_dt}"
        )
        raw_transactions = self._transaction_extractor.extract(
            start_dt=start_dt, end_dt=end_dt
        )
        logger.debug(f"Transforming transactions")
        transactions = self._transaction_transformer.transform(raw_transactions)
        logger.debug(f"Loading transactions into database")
        self._transaction_loader.load(transactions)
        logger.debug(f"Committing transactions")
        self._transaction_dao.commit()
        logger.info(f"Transaction ETL complete")
