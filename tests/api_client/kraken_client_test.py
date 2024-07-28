import datetime
from unittest.mock import MagicMock

from lightpms.api_client.kraken_client import KrakenClient
from lightpms.model.models import Asset, AssetType


def test_get_transactions():
    start_dt = datetime.datetime(2023, 10, 1)
    end_dt = datetime.datetime(2024, 1, 31)
    execution_1 = {
        "uid": "abc1",
        "order": {},
        "timestamp": "1706546109527",
        "quantity": "10.0",
        "price": "1.00",
        "markPrice": "1.00",
        "limitFilled": True,
        "executionType": "maker",
        "usdValue": "10.00",
        "orderData": {},
    }
    execution_2 = {
        "uid": "abc2",
        "order": {},
        "timestamp": "1706546109525",
        "quantity": "20.0",
        "price": "1.00",
        "markPrice": "1.00",
        "limitFilled": False,
        "executionType": "maker",
        "usdValue": "20.00",
        "orderData": {},
    }
    history_executions = {
        "elements": [
            {"event": {"execution": {"execution": execution_1}}},
            {"event": {"execution": {"execution": execution_2}}},
        ]
    }
    ccxt_exchange = MagicMock()
    ccxt_exchange.history_get_executions.return_value = history_executions
    client = KrakenClient(ccxt_exchange)

    transactions = client.get_transactions(start_dt, end_dt)

    expected_transactions = [execution_1, execution_2]
    assert transactions == expected_transactions


def test_get_asset_info():
    asset = Asset(a_name="BTC/USD", a_type=AssetType.PERPETUAL)
    expected_asset_info = {"symbol": "BTC/USD", "precision": 8}
    ccxt_exchange = MagicMock()
    ccxt_exchange.load_markets.return_value = {"BTC/USD": expected_asset_info}
    client = KrakenClient(ccxt_exchange)

    asset_info = client.get_asset_info(asset)

    assert asset_info == expected_asset_info
    ccxt_exchange.load_markets.assert_called_once()
