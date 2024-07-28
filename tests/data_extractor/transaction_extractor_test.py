import datetime
from unittest.mock import MagicMock

import pytest

from lightpms.api_client.kraken_client import KrakenClient
from lightpms.data_extractor.transaction_extractor import TransactionExtractor


@pytest.mark.skip("Run on demand")
def test_acceptance_extract(ccxt_exchange):
    start_dt = datetime.datetime(2023, 10, 1)
    end_dt = datetime.datetime(2024, 1, 31)

    api_client = KrakenClient(ccxt_exchange)

    transaction_extractor = TransactionExtractor(api_client)

    raw_transactions = list(t for t in transaction_extractor.extract(start_dt, end_dt))

    assert len(raw_transactions) > 0


def test_extract(historical_execution):
    start_dt = datetime.datetime(2023, 10, 1)
    end_dt = datetime.datetime(2024, 1, 31)

    api_client = MagicMock()

    # Mocking the get_transactions method of the api_client
    api_client.get_transactions.return_value = [historical_execution] * 2

    transaction_extractor = TransactionExtractor(api_client)

    raw_transactions = list(t for t in transaction_extractor.extract(start_dt, end_dt))

    assert len(raw_transactions) == 2

    api_client.get_transactions.assert_called_once_with(
        start_dt=start_dt, end_dt=end_dt
    )
