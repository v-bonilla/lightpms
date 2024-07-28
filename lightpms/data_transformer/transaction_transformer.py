import datetime
import logging
from typing import Any, Dict, Generator

from lightpms.dao.daos import AssetDAO
from lightpms.data_transformer.data_transformer import DataTransformer
from lightpms.model.models import Asset, AssetType, Transaction

logger = logging.getLogger(__name__)


class TransactionTransformer(DataTransformer):
    def __init__(self, asset_dao: AssetDAO) -> None:
        super().__init__()
        self._asset_dao = asset_dao

    def transform(
        self, raw_transactions: Generator[Dict, Any, None]
    ) -> Generator[Transaction, Any, None]:
        logger.debug(f"Transforming raw_transactions")
        for transaction in raw_transactions:
            logger.debug(f"Processing transaction: {transaction}")
            asset_name = transaction["order"]["tradeable"]
            if asset_name is not None and isinstance(asset_name, str):
                logger.debug(f"Got transaction for asset {asset_name}")
                asset = self._asset_dao.get_by_name(name=asset_name)
                if asset is None:
                    logger.debug(f"Asset {asset_name} not found, creating new asset")
                    asset = Asset(a_name=asset_name, a_type=AssetType.PERPETUAL)
                    a_id = self._asset_dao.insert_asset(a=asset)
                else:
                    logger.debug(f"Asset {asset_name} found in database")
                    a_id = asset.a_id
                transaction_datetime = (
                    datetime.datetime.utcfromtimestamp(  # data comes in UTC
                        int(transaction["timestamp"]) / 1000
                    )
                )
                transaction_date = (
                    transaction_datetime.date()
                )  # datetime.date doesn't have tz functionality
                transaction_type = transaction["order"]["direction"].lower()
                transaction_quantity = float(transaction["quantity"])
                transaction_price = float(transaction["price"])
                t = Transaction(
                    a_id=a_id,
                    t_date=transaction_date,
                    t_type=transaction_type,
                    t_quantity=transaction_quantity,
                    t_price=transaction_price,
                )
                self.validate_datapoint(t=t)
                yield t

    def validate_datapoint(self, t: Transaction) -> None:
        logger.debug(f"Validating transaction: {repr(t)}")
        if not isinstance(t.a_id, int) or t.a_id <= 0:
            raise ValueError("Asset ID must be a positive integer")
        if not isinstance(t.t_date, datetime.date):
            raise ValueError("Transaction date must be a datetime.date instance")
        if t.t_type not in ["buy", "sell"]:
            raise ValueError("Transaction type must be either 'buy' or 'sell'")
        if not isinstance(t.t_quantity, float) or t.t_quantity <= 0:
            raise ValueError("Transaction quantity must be a positive number")
        if not isinstance(t.t_price, float) or t.t_price <= 0:
            raise ValueError("Transaction price must be a positive number")
