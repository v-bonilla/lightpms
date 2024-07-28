import datetime
from typing import Dict, List, Optional

import ccxt

from lightpms.api_client.api_client import APIClient
from lightpms.model.models import Asset


class KrakenClient(APIClient):
    """API Client for Kraken."""

    def __init__(self, ccxt_exchange: ccxt.Exchange) -> None:
        super().__init__()
        self._ccxt_exchange = ccxt_exchange

    def get_transactions(
        self, start_dt: datetime.datetime, end_dt: datetime.datetime
    ) -> List[Dict[str, str | Dict]]:
        """Downloads transactions in the account for the given period.

        Query implicit API endpoint as of today, getting all info of trades is not supported by ccxt unified API.

        Response schemas:

        - HistoricalExecution
        Type: Object
        Object Fields:
            Field: limitFilled
                Type/Data Type: Optional Boolean
            Field: makerOrder
                Type/Data Type: Optional HistoricalOrder
            Field: makerOrderData
                Type/Data Type: Optional MakerOrderData
            Field: markPrice
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: oldTakerOrder
                Type/Data Type: Optional HistoricalOrder
            Field: price
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: quantity
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: takerOrder
                Type/Data Type: Optional HistoricalOrder
            Field: takerOrderData
                Type/Data Type: Optional TakerOrderData
            Field: timestamp
                ** Currently, this is a string in the API response. **
                Type/Data Type: Optional String (format: timestamp-milliseconds)
                Example: "1604937694000"
            Field: uid
                Type/Data Type: Optional String (format: uuid)
            Field: usdValue
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"

        Currently, fields makerOrder, makerOrderData, oldTakerOrder, takerOrder, takerOrderData are not
        returned by the API. Instead, fields order and orderData are returned. Description of these fields:

        - HistoricalOrder
        Type: Object
        Object Fields:
            Field: accountUid
                Type/Data Type: Optional String (format: uuid)
            Field: clientId
                Type/Data Type: Optional String
            Field: direction
                Type/Data Type: Optional String (enum: "Buy", "Sell")
            Field: filled
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: lastUpdateTimestamp
                Type/Data Type: Optional String (format: timestamp-milliseconds)
                Example: "1604937694000"
            Field: limitPrice
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: orderType
                Type/Data Type: Optional String (enum: "Limit", "IoC", "Post", "Market", "Liquidation", "Assignment", "Unwind")
            Field: quantity
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: reduceOnly
                Type/Data Type: Optional Boolean
            Field: spotData
                Type/Data Type: Optional (Null or String)
            Field: timestamp
                Type/Data Type: Optional String (format: timestamp-milliseconds)
                Example: "1604937694000"
            Field: tradeable
                Type/Data Type: Optional String
            Field: uid
                Type/Data Type: Optional String (format: uuid)

        - OrderData
        Type: Object
        Object Fields:
            Field: fee
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
            Field: positionSize
                Type/Data Type: Optional String (format: big-decimal)
                Example: "1234.56789"
        """
        executions_response = self._ccxt_exchange.history_get_executions()  # type: ignore
        start_ts = start_dt.timestamp() * 1000
        end_ts = end_dt.timestamp() * 1000
        transactions = [
            e["event"]["execution"]["execution"]
            for e in executions_response["elements"]
            if float(e["event"]["execution"]["execution"]["timestamp"]) >= start_ts
            and float(e["event"]["execution"]["execution"]["timestamp"]) <= end_ts
        ]
        return transactions

    def get_asset_info(self, asset: Asset) -> Optional[Dict]:
        """Downloads asset info."""
        asset_info = self._ccxt_exchange.load_markets().get(asset.a_name)
        return asset_info

    def get_daily_close_price(
        self, asset: Asset, start_dt: datetime.datetime, end_dt: datetime.datetime
    ) -> List[Dict]:
        """Downloads daily close price for the given asset and period."""
        raise NotImplementedError
