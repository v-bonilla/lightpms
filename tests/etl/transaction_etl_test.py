import datetime
import logging
import time
from unittest.mock import MagicMock

import pytest

from lightpms.api_client.kraken_client import KrakenClient
from lightpms.dao.daos import AssetDAO, TransactionDAO
from lightpms.data_extractor.transaction_extractor import TransactionExtractor
from lightpms.data_loader.transaction_loader import TransactionLoader
from lightpms.data_transformer.transaction_transformer import TransactionTransformer
from lightpms.etl.transaction_etl import TransactionETL
from lightpms.logger.logger import setup_logging


@pytest.mark.skip("Run on demand")
def test_acceptance_transaction_etl(db_session, ccxt_exchange):
    setup_logging(logging.DEBUG)
    logger = logging.getLogger(__name__)

    start_dt = datetime.datetime(2023, 10, 1)
    end_dt = datetime.datetime(2024, 1, 31)

    api_client = KrakenClient(ccxt_exchange)
    asset_dao = AssetDAO(db_session)
    transaction_dao = TransactionDAO(db_session)

    transaction_extractor = TransactionExtractor(api_client)
    transaction_transformer = TransactionTransformer(asset_dao)
    transaction_loader = TransactionLoader(transaction_dao)

    etl = TransactionETL(
        transaction_extractor=transaction_extractor,
        transaction_transformer=transaction_transformer,
        transaction_loader=transaction_loader,
        transaction_dao=transaction_dao,
    )
    logger.info(f"Running transaction ETL from {start_dt} to {end_dt}")
    start = time.time()
    etl.run(start_dt, end_dt)
    end = time.time()
    logger.info(f"Time taken: {end - start}")


def test_transaction_etl():
    start_dt = datetime.datetime(2023, 10, 1)
    end_dt = datetime.datetime(2024, 1, 31)

    transaction_extractor = MagicMock()
    transaction_transformer = MagicMock()
    transaction_loader = MagicMock()
    transaction_dao = MagicMock()

    etl = TransactionETL(
        transaction_extractor=transaction_extractor,
        transaction_transformer=transaction_transformer,
        transaction_loader=transaction_loader,
        transaction_dao=transaction_dao,
    )

    etl.run(start_dt, end_dt)

    transaction_extractor.extract.assert_called_once_with(
        start_dt=start_dt, end_dt=end_dt
    )
    transaction_transformer.transform.assert_called_once_with(
        transaction_extractor.extract.return_value
    )
    transaction_loader.load.assert_called_once_with(
        transaction_transformer.transform.return_value
    )
    transaction_dao.commit.assert_called_once()
