from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., ge=1)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    ...


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example='В добрые руки.')
    description: Optional[str] = Field(None, min_length=1, example='Оплата передержки животных.')
    full_amount: Optional[int] = Field(None, ge=1)

    @validator('name', 'description', 'full_amount')
    def required_fields(cls, value):
        if value is None:
            raise ValueError(
                'Имя проекта, описание или взнос не могут быть пустыми.'
            )
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
