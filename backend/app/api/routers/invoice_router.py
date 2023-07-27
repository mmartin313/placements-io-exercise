from typing import Optional
from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.db.crud.campaign import get_campaigns, get_campaign
from app.db.crud.line_item import get_line_item, get_line_items, edit_line_item
from app.db.schemas import CampaignSchema, LineItemSchema, LineItemEditSchema


invoice_router = r = APIRouter()


@r.get(
    "/campaigns",
    response_model=list[CampaignSchema],
)
async def campaign_list(
    db=Depends(get_db),
):
    """
    Get all Campaigns
    """
    campaigns = get_campaigns(db)
    return campaigns


@r.get(
    "/campaigns/{campaign_id}",
    response_model=CampaignSchema,
)
async def campaign_single(
    campaign_id: int,
    db=Depends(get_db),
):
    """
    Get any single Campaign by id
    """
    return get_campaign(db, campaign_id)


@r.get(
    "/line-items",
    response_model=list[LineItemSchema],
)
async def line_item_list(
    campaign_id: Optional[int] = None,
    db=Depends(get_db),
):
    """
    Get all Line Items
    """
    filters: dict = {}

    if campaign_id:
        filters["campaign_id"] = campaign_id

    if campaign_id:
        {"campaign_id": campaign_id}
    line_items = get_line_items(db, filters=filters)
    return line_items


@r.get(
    "/line-items/{line_item_id}",
    response_model=LineItemSchema,
)
async def line_item_single(
    line_item_id: int,
    db=Depends(get_db),
):
    """
    Get any single Line Item by id
    """
    return get_line_item(db, line_item_id)


@r.patch(
    "/line-items/{line_item_id}",
    response_model=LineItemSchema,
)
async def line_item_edit(
    line_item_id: int,
    line_item_edit_data: LineItemEditSchema,
    db=Depends(get_db),
):
    """
    Update existing Line Item
    """

    return edit_line_item(db, line_item_id, line_item_edit_data)
