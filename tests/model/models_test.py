"""Simple test for ORM models creating a disposable PostgreSQL DB under `/tmp`."""

import datetime

from sqlalchemy import select

from lightpms.dao.daos import TransactionDAO
from lightpms.model.models import Transaction
from lightpms.model.models_tables import transaction_table


def test_insert_two_transactions_with_dao(db_session):
    btc_transaction = Transaction(
        p_id=1,
        a_id=1,
        t_date=datetime.date(2023, 12, 1),
        t_type="buy",
        t_quantity=10.0,
        t_price=37000.0,
    )
    eth_transaction = Transaction(
        p_id=1,
        a_id=2,
        t_date=datetime.date(2023, 12, 1),
        t_type="buy",
        t_quantity=100.0,
        t_price=2000.0,
    )
    t_dao = TransactionDAO(db_session)
    t_dao.insert_transactions([btc_transaction, eth_transaction])
    db_session.flush()

    # Query the transaction within the same session where portfolio_id = 1 and date = 2023-12-01
    stmt = (
        select(
            transaction_table.c.t_id,
            transaction_table.c.p_id,
            transaction_table.c.a_id,
            transaction_table.c.t_date,
            transaction_table.c.t_type,
            transaction_table.c.t_quantity,
            transaction_table.c.t_price,
        )
        .where(transaction_table.c.p_id == 1)
        .where(transaction_table.c.t_date == datetime.datetime(2023, 12, 1))
    )
    cursor_result = db_session.execute(stmt)
    result = [
        Transaction(
            t_id=row.t[0],
            p_id=row.t[1],
            a_id=row.t[2],
            t_date=row.t[3],
            t_type=row.t[4],
            t_quantity=float(row.t[5]),
            t_price=float(row.t[6]),
        )
        for row in cursor_result
    ]

    # Assert that the transaction was inserted
    assert len(result) == 2
    result_no_t_id = [
        Transaction(
            p_id=r.p_id,
            a_id=r.a_id,
            t_date=r.t_date,
            t_type=r.t_type,
            t_quantity=float(r.t_quantity),
            t_price=float(r.t_price),
        )
        for r in result
    ]
    assert btc_transaction in result_no_t_id and eth_transaction in result_no_t_id
