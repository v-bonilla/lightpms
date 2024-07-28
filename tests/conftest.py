import ccxt
import pytest

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

from lightpms.config.config_manager import ConfigManager, Environment


@pytest.fixture
def config_manager():
    return ConfigManager(Environment.DEV)


@pytest.fixture
def db_session(config_manager):
    host = config_manager.get_postgres_host()
    database = config_manager.get_postgres_database()
    username = config_manager.get_postgres_user()
    password = config_manager.get_postgres_password()

    url = URL.create(
        drivername="postgresql",
        host=host,
        database=database,
        username=username,
        password=password,
    )

    engine = create_engine(url, echo=True)
    session = Session(engine)
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def ccxt_exchange(config_manager):
    api_key = config_manager.get_exchange_api_key()
    secret_key = config_manager.get_exchange_secret_key()
    ccxt_exchange = ccxt.krakenfutures(
        {
            "apiKey": api_key,
            "secret": secret_key,
        }
    )
    return ccxt_exchange


@pytest.fixture
def order_data():
    return {"fee": "1234.56789", "positionSize": "1234.56789"}


@pytest.fixture(
    params=[
        ("PF_BTCUSD", "Buy", "Limit"),
        ("PF_ETHUSD", "Buy", "Liquidation"),
        ("PF_BTCUSD", "Sell", "Limit"),
        ("PF_ETHUSD", "Sell", "Liquidation"),
    ]
)
def historical_order(request):
    tradeable, direction, orderType = request.param
    return {
        "accountUid": "123e4567-e89b-12d3-a456-426614174000",
        "clientId": "",
        "direction": direction,
        "filled": "1234.56789",
        "lastUpdateTimestamp": "1604937694000",
        "limitPrice": "1234.56789",
        "orderType": orderType,
        "quantity": "1234.56789",
        "reduceOnly": False,
        "spotData": None,
        "timestamp": "1604937694000",
        "tradeable": tradeable,
        "uid": "123e4567-e89b-12d3-a456-426614174001",
    }

@pytest.fixture
def historical_execution(historical_order, order_data):
    return {
        "limitFilled": True,
        "order": historical_order,
        "markPrice": "1234.56789",
        "price": "1234.56789",
        "quantity": "1234.56789",
        "orderData": order_data,
        "timestamp": "1604937694000",
        "uid": "123e4567-e89b-12d3-a456-426614174002",
        "usdValue": "1234.56789",
    }
