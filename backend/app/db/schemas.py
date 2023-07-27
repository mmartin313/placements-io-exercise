from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    created_on: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"


class CampaignSchema(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    is_reviewed: bool
    total_billable_amount: Decimal


class LineItemSchema(BaseModel):
    class Config:
        orm_mode = True

    id: int
    name: str
    campaign_id: int
    campaign: CampaignSchema
    booked_amount: Decimal
    actual_amount: Decimal
    adjustments: Decimal
    billable_amount: Decimal
    billable_amount_euro: Optional[Decimal]
    is_reviewed: bool
    is_archived: bool


class LineItemEditSchema(BaseModel):
    name: Optional[str]
    campaign_id: Optional[int]
    booked_amount: Optional[Decimal]
    actual_amount: Optional[Decimal]
    adjustments: Optional[str]
    is_reviewed: Optional[bool]
    is_archived: Optional[bool]
