from abc import ABC, abstractmethod
import datetime
from typing import Dict, List, Optional
from lightpms.model.models import Asset


class APIClient(ABC):
    """API Client that downloads transactions, asset information and market data."""

    @abstractmethod
    def get_transactions(self, start_dt: datetime.datetime, end_dt: datetime.datetime) -> List[Dict[str, str | Dict]]:
        """Downloads transactions in the account for the given period."""

    @abstractmethod
    def get_asset_info(self, asset: Asset) -> Optional[Dict]:
        """Downloads asset info."""

    @abstractmethod
    def get_daily_close_price(self, asset: Asset, start_dt: datetime.datetime, end_dt: datetime.datetime) -> List[Dict]:
        """Downloads daily close price for the given asset and period."""
