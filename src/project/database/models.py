from sqlalchemy import Column, Integer, Float, String, DateTime, Date
from sqlalchemy import UniqueConstraint
from .base import BaseAPI, BaseTSDB


class ExpectedMove(BaseAPI):
    __tablename__ = "expected_moves"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False, index=True)
    trade_date = Column(Date, nullable=False, index=True)
    underlying_price = Column(Float)
    expected_move = Column(Float)
    sigma2_up = Column(Float)
    sigma1_up = Column(Float)
    sigma1_down = Column(Float)
    sigma2_down = Column(Float)
    timestamp = Column(DateTime)
    type = Column(String, nullable=False, index=True)

    # Add a unique constraint to prevent duplicates
    __table_args__ = (UniqueConstraint('symbol', 'trade_date', 'type', name='uix_1'),)