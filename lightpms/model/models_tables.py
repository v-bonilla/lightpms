from sqlalchemy import (
    DECIMAL,
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

metadata = MetaData()

portfolio_table = Table(
    "portfolio",
    metadata,
    Column("p_id", Integer, primary_key=True),
    Column("p_name", String(255)),
    Column("p_description", String),
    Column("p_creation_date", Date),
)

asset_table = Table(
    "asset",
    metadata,
    Column("a_id", Integer, primary_key=True),
    Column("a_name", String(255)),
    Column("a_type", String(255)),
)

transaction_table = Table(
    "transaction",
    metadata,
    Column("t_id", Integer, primary_key=True),
    Column("p_id", Integer, ForeignKey("portfolio.p_id")),
    Column("a_id", Integer, ForeignKey("asset.a_id")),
    Column("t_date", Date),
    Column("t_type", String(10)),
    Column("t_quantity", DECIMAL),
    Column("t_price", DECIMAL),
)

market_data_table = Table(
    "market_data",
    metadata,
    Column("md_id", Integer, primary_key=True),
    Column("a_id", Integer, ForeignKey("asset.a_id")),
    Column("md_date", Date),
    Column("md_open_price", DECIMAL),
    Column("md_close_price", DECIMAL),
    Column("md_volume", DECIMAL),
)

benchmark_table = Table(
    "benchmark",
    metadata,
    Column("b_id", Integer, primary_key=True),
    Column("b_name", String(255)),
    Column("b_type", String(255)),
)

benchmark_data_table = Table(
    "benchmark_data",
    metadata,
    Column("bd_id", Integer, primary_key=True),
    Column("b_id", Integer, ForeignKey("benchmark.b_id")),
    Column("bd_date", Date),
    Column("bd_value", DECIMAL),
)

risk_metrics_table = Table(
    "risk_metrics",
    metadata,
    Column("rm_id", Integer, primary_key=True),
    Column("p_id", Integer, ForeignKey("portfolio.p_id")),
    Column("rm_date", Date),
    Column("rm_var95", DECIMAL),
    Column("rm_var99", DECIMAL),
    Column("rm_std", DECIMAL),
    Column("rm_beta", DECIMAL),
)

portfolio_asset_table = Table(
    "portfolio_asset",
    metadata,
    Column("p_id", Integer, ForeignKey("portfolio.p_id"), primary_key=True),
    Column("a_id", Integer, ForeignKey("asset.a_id"), primary_key=True),
    Column("pa_quantity", DECIMAL),
)
