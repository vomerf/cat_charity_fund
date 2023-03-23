from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Extra, Field


class DonationCreate(BaseModel):
    full_amount: int = Field(..., ge=1)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int

    class Config:
        orm_mode = True
