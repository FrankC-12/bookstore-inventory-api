from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    cost_usd: float
    selling_price_local: float
    stock_quantity: int
    category: str
    supplier_country: str
    created_at: Optional[date]
    updated_at: Optional[date]
    model_config = {
        "from_attributes": True
    }


class BookCreate(BaseModel):
    title: str = Field(..., example="The Great Gatsby")
    author: str = Field(..., example="F. Scott Fitzgerald")
    isbn: str = Field(..., example="9780743273565")
    cost_usd: float = Field(..., example=10.99)
    selling_price_local: float = Field(..., example=15.99)
    stock_quantity: int = Field(..., example=100)
    category: str = Field(..., example="Fiction")
    supplier_country: str = Field(..., example="USA")
    created_at: Optional[date] = Field(None, example="1925-04-10")
    updated_at: Optional[date] = Field(None, example="2024-01-01")

    @field_validator('cost_usd', 'selling_price_local', 'stock_quantity')
    def non_negative(cls, v):
        if v < 0:
            raise ValueError('Must be non-negative')
        return v

    @field_validator('isbn')
    def valid_isbn(cls, v):
        if len(v) not in [10, 13] or not v.isdigit():
            raise ValueError('ISBN must be 10 or 13 digits')
        return v

class BookUpdate(BaseModel):
    author: str = Field(..., example="F. Scott Fitzgerald")
    isbn: str = Field(..., example="9780743273565")
    cost_usd: float = Field(..., example=10.99)
    selling_price_local: float = Field(..., example=15.99)
    stock_quantity: int = Field(..., example=100)
    category: str = Field(..., example="Fiction")
    supplier_country: str = Field(..., example="USA")
    created_at: Optional[date] = Field(None, example="1925-04-10")
    updated_at: Optional[date] = Field(None, example="2024-01-01")

    @field_validator('cost_usd', 'selling_price_local', 'stock_quantity')
    def non_negative(cls, v):
        if v < 0:
            raise ValueError('Must be non-negative')
        return v

    @field_validator('isbn')
    def valid_isbn(cls, v):
        if len(v) not in [10, 13] or not v.isdigit():
            raise ValueError('ISBN must be 10 or 13 digits')
        return v



