import logging
from typing import Any, Generator, List, Optional, TypeVar

from sqlalchemy import insert, select

from lightpms.model.models import Asset, Transaction
from lightpms.model.models_tables import asset_table, transaction_table

logger = logging.getLogger(__name__)


T = TypeVar("T")


class BaseDAO:
    """
    Base repository class for managing objects in the database.

    This class includes a cache for inserted but uncommitted objects. The cache is used to
    store objects that have been inserted into the database but whose transactions have not
    yet been committed. This allows other parts of the application to retrieve these objects
    without needing to commit the transaction first. This is particularly useful in scenarios
    where multiple related objects need to be inserted in a single transaction, and these
    objects need to be retrievable immediately after they are inserted.

    The cache is cleared when the transaction is committed, ensuring that it does not hold
    onto objects from previous transactions.
    """

    def __init__(self, session):
        self._session = session
        self._cache = {}  # Cache for inserted but uncommitted objects

    def add_to_cache(self, key: str, value: T):
        logger.debug(f"Adding {key} -> {repr(value)} to cache")
        self._cache[key] = value

    def get_from_cache(self, key: str) -> Optional[T]:
        logger.debug(f"Getting {key} from cache")
        return self._cache.get(key)

    def commit(self):
        logger.debug(f"Committing transactions")
        self._session.commit()
        logger.debug(f"Clearing cache")
        self._cache.clear()  # Clear the cache after committing


class AssetDAO(BaseDAO):
    """
    Repository class for managing assets in the database.
    """

    def get_by_name(self, name: str) -> Optional[Asset]:
        """
        Retrieves an asset from the database by its name.

        Args:
            name (str): The name of the asset.

        Returns:
            Optional[Asset]: The asset if found, None otherwise.
        """
        logger.debug(f"Getting asset with name {name}")
        # First, check the cache
        asset = self.get_from_cache(name)
        if asset is not None:
            return asset

        logger.debug(f"Asset {name} not found in cache")
        # If not in the cache, query the database
        stmt = select(asset_table).where(asset_table.c.a_name == name)
        logger.debug(f"Executing query: {stmt}")
        cursor_result = self._session.execute(stmt)
        result = [
            Asset(
                a_id=row[0],
                a_name=row[1],
                a_type=row[2],
            )
            for row in cursor_result
        ]
        logger.debug(f"Query result: {result}")
        if len(result) == 0:
            return None
        elif len(result) == 1:
            return result[0]
        else:
            raise Exception("More than one asset found with the same name")

    def insert_asset(self, a: Asset) -> int:
        """
        Inserts an asset into the database.

        Args:
            a (Asset): The asset object to be inserted.

        Returns:
            int: The primary key of the inserted asset.
        """
        logger.debug(f"Inserting asset {repr(a)}")
        a_dict = a.to_dict()
        if a.a_id is None:
            del a_dict["a_id"]
        logger.debug(f"Inserting asset with dict: {a_dict}")
        result = self._session.execute(
            insert(asset_table),
            a_dict,
        )
        if result.inserted_primary_key is None:
            raise Exception("Primary key of insertion can't be None")
        a_id: int = result.inserted_primary_key[0]
        logger.debug(f"Inserted asset with id {a_id}")
        a.a_id = a_id  # Update the asset object with the primary key
        logger.debug(f"Adding {repr(a)} to cache")
        self.add_to_cache(a.a_name, a)  # Add the asset to the cache
        return a_id


class TransactionDAO(BaseDAO):
    """
    Repository class for managing transactions in the database.
    """

    def insert_transactions(
        self, transactions: List[Transaction] | Generator[Transaction, Any, None]
    ) -> List[int]:
        """
        Inserts a list of transactions into the database.

        Args:
            transactions (List[Transaction]): The list of transactions to be inserted.

        Returns:
            List[int]: The list of primary keys of the inserted transactions.
        """
        logger.debug(f"Inserting transactions")
        t_dicts = []
        for t in transactions:
            t_dict = t.to_dict()
            # If t_id is None, remove it from the dict and let the database generate it
            if t_dict["t_id"] is None:
                del t_dict["t_id"]
            logger.debug(f"Inserting transaction with dict: {t_dict}")
            t_dicts.append(t_dict)

        result = self._session.execute(
            insert(transaction_table).returning(transaction_table.c.t_id),
            t_dicts,
        )
        ids = [row[0] for row in result]
        logger.debug(f"Inserted transactions with ids {ids}")
        if any(_id is None for _id in ids):
            raise Exception("Primary key of insertion can't be None")
        return ids
