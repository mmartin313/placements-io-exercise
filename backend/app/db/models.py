from decimal import Decimal
import os

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, DECIMAL, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import requests

from app.db.session import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    last_modified = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class User(BaseModel):
    __tablename__ = "user"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Campaign(BaseModel):
    __tablename__ = "campaign"

    name = Column(String)
    is_reviewed = Column(Boolean, server_default="0", nullable=False)
    line_items = relationship("LineItem")

    @property
    def total_billable_amount(self):
        return sum([line_item.billable_amount for line_item in self.line_items])


class LineItem(BaseModel):
    __tablename__ = "line_item"

    name = Column(String)
    campaign_id = Column(Integer, ForeignKey("campaign.id"))
    campaign = relationship("Campaign")
    booked_amount = Column(DECIMAL(22, 12), default=0.0)
    actual_amount = Column(DECIMAL(22, 12), default=0.0)
    adjustments = Column(DECIMAL(22, 12), default=0.0)
    is_reviewed = Column(Boolean, server_default="0", nullable=False)
    is_archived = Column(Boolean, server_default="0", nullable=False)

    @property
    def billable_amount(self):
        return Decimal(self.actual_amount + self.adjustments)

    # Ideally this value would be cached somewhere, currently it will burn through the API rate limit
    @property
    def billable_amount_euro(self):
        try:
            response = requests.get(
                "http://data.fixer.io/api/latest",
                {
                    "access_key": os.environ.get("FIXER_API_KEY"),
                    "symbols": "GBP,JPY,EUR, USD",
                },
            )
            print(response.json())
            rate = response.json()["rates"]["USD"]
            return self.billable_amount / Decimal(rate)
        except Exception as e:
            return None
