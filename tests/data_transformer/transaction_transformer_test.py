import datetime
from lightpms.dao.daos import AssetDAO
from lightpms.data_transformer.transaction_transformer import TransactionTransformer
from lightpms.model.models import Transaction


def test_acceptance_transform(db_session, historical_execution):
    asset_dao = AssetDAO(db_session)
    transaction_transformer = TransactionTransformer(asset_dao)

    raw_transactions = [historical_execution] * 3

    transformed_transactions = list(transaction_transformer.transform(raw_transactions))

    assert len(transformed_transactions) == 3
    assert all(isinstance(t, Transaction) for t in transformed_transactions)
    assert all(
        t.a_id is not None and isinstance(t.a_id, int) for t in transformed_transactions
    )
    assert all(
        t.t_date is not None and isinstance(t.t_date, datetime.date)
        for t in transformed_transactions
    )
    assert all(
        t.t_type is not None and isinstance(t.t_type, str)
        for t in transformed_transactions
    )
    assert all(
        t.t_quantity is not None and isinstance(t.t_quantity, float)
        for t in transformed_transactions
    )
    assert all(
        t.t_price is not None and isinstance(t.t_price, float)
        for t in transformed_transactions
    )
