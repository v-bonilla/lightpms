# pylint: disable=missing-module-docstring, missing-class-docstring, too-few-public-methods
import datetime
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Optional


@dataclass
class BaseModelDC:
    def to_dict(self):
        return asdict(self)


@dataclass
class Portfolio(BaseModelDC):
    p_name: str
    p_description: str
    p_creation_date: datetime.date
    p_id: Optional[int] = None


class AssetType(Enum):
    PERPETUAL = "perpetual"


@dataclass
class Asset(BaseModelDC):
    a_name: str
    a_type: AssetType
    a_id: Optional[int] = None

    def to_dict(self):
        a_dict = super().to_dict()
        a_dict["a_type"] = a_dict["a_type"].value
        return a_dict


@dataclass
class Transaction(BaseModelDC):
    t_date: datetime.date
    t_type: str
    t_quantity: float
    t_price: float
    t_id: Optional[int] = None
    p_id: Optional[int] = None
    a_id: Optional[int] = None


@dataclass
class MarketData(BaseModelDC):
    md_date: datetime.date
    md_open_price: float
    md_close_price: float
    md_volume: float
    md_id: Optional[int] = None
    a_id: Optional[int] = None


@dataclass
class Benchmark(BaseModelDC):
    b_name: str
    b_type: str
    b_id: Optional[int] = None


@dataclass
class BenchmarkData(BaseModelDC):
    bd_date: datetime.date
    bd_value: float
    bd_id: Optional[int] = None
    b_id: Optional[int] = None


@dataclass
class RiskMetrics(BaseModelDC):
    rm_date: datetime.date
    rm_var95: float
    rm_var99: float
    rm_std: float
    rm_beta: float
    rm_id: Optional[int] = None
    p_id: Optional[int] = None
