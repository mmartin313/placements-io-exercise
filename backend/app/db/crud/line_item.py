from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models import LineItem
from app.db.schemas import (
    LineItemEditSchema,
    LineItemSchema,
)


def get_line_items(db: Session, filters: dict) -> list[LineItemSchema]:
    query = db.query(LineItem)

    if filters:
        query = query.filter_by(**filters)

    return query.all()


def get_line_item(db: Session, line_item_id: int):
    line_item = db.query(LineItem).filter(LineItem.id == line_item_id).one_or_none()
    if not line_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Line item not found")
    return line_item


def edit_line_item(
    db: Session,
    line_item_id: int,
    line_item_update_data: LineItemEditSchema,
) -> LineItemSchema:
    line_item = get_line_item(db, line_item_id)

    if (line_item.is_reviewed or line_item.campaign.is_reviewed) and (
        line_item_update_data.is_reviewed is None
    ):
        raise HTTPException(
            status_code=400, detail="Unable to edit a reviewed line item"
        )

    update_data = line_item_update_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(line_item, key, value)

    db.add(line_item)
    db.commit()
    db.refresh(line_item)
    return line_item
