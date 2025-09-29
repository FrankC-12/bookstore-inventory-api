from pydantic import BaseModel, field_validator
from datetime import datetime

class ExchangeRequest(BaseModel):
    amount: float
    from_currency: str
    to_currency: str

    @field_validator('amount')
    def non_negative(cls, v):
        if v < 0:
            raise ValueError('Amount must be non-negative')
        return v

class ExchangeResponse(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    exchange_rate: float
    converted_amount: float
    calculation_timestamp: datetime
    model_config = {
        "from_attributes": True
    }