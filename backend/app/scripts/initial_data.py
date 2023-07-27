#!/usr/bin/env python3
import json

from app.db.crud.user import create_user
from app.db.models import Campaign, LineItem
from app.db.schemas import UserCreate
from app.db.session import SessionLocal


def init_users() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="user1@example.com",
            password="user1password",
        ),
    )

    create_user(
        db,
        UserCreate(
            email="user2@example.com",
            password="user2password",
        ),
    )


def init_data() -> None:
    db = SessionLocal()

    with open("app/scripts/placements_teaser_data.json") as jsonfile:
        data = json.load(jsonfile)

        for line_item_data in data:
            # Create Campaign
            campaign = (
                db.query(Campaign)
                .filter(Campaign.id == line_item_data.get("campaign_id"))
                .one_or_none()
            )

            if not campaign:
                campaign = Campaign(
                    id=line_item_data.get("campaign_id"),
                    name=line_item_data.get("campaign_name"),
                )

                db.add(campaign)
                db.flush()

            # Create Line Item
            existing_line_item = (
                db.query(LineItem)
                .filter(LineItem.name == line_item_data.get("line_item_name"))
                .one_or_none()
            )

            if not existing_line_item:
                new_line_item = LineItem(
                    id=line_item_data.get("id"),
                    name=line_item_data.get("line_item_name"),
                    campaign_id=campaign.id,
                    booked_amount=line_item_data.get("booked_amount"),
                    actual_amount=line_item_data.get("actual_amount"),
                    adjustments=line_item_data.get("adjustments"),
                )

                db.add(new_line_item)
                db.flush()

        db.commit()


if __name__ == "__main__":
    print("Creating test users...")
    init_users()
    print("Test users created")

    print("Starting population script...")
    init_data()
    print("Population script complete!")
