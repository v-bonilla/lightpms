import datetime
import logging
from typing import Any, Dict, Generator

from lightpms.api_client.api_client import APIClient
from lightpms.data_extractor.data_extractor import DataExtractor

logger = logging.getLogger(__name__)


class TransactionExtractor(DataExtractor):
    def __init__(self, api_client: APIClient) -> None:
        super().__init__()
        self._api_client = api_client

    def extract(
        self, start_dt: datetime.datetime, end_dt: datetime.datetime
    ) -> Generator[Dict, Any, None]:
        logger.debug(f"Extracting transactions from {start_dt} to {end_dt}")
        transactions = self._api_client.get_transactions(
            start_dt=start_dt, end_dt=end_dt
        )
        if transactions:
            logger.debug(f"Extracted {len(transactions)} transactions")
            for transaction in transactions:
                yield transaction
