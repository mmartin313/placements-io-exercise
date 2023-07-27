from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import Campaign


def get_campaigns(
    db: Session,
) -> list[Campaign]:
    query = db.query(Campaign)
    return query.all()


def get_campaign(
    db: Session,
    campaign_id: int,
) -> Campaign:
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).one_or_none()
    if not campaign:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Campaign not found")
    return campaign
