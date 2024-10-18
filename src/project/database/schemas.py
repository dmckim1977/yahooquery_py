from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ExpectedMoveBase(BaseModel):
    symbol: str
    underlying_price: float
    expected_move: float
    sigma2_up: float
    sigma1_up: float
    sigma1_down: float
    sigma2_down: float
    type: str

class ExpectedMoveCreate(ExpectedMoveBase):
    pass

class ExpectedMove(ExpectedMoveBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)