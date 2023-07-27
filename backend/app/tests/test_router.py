from app.db.models import Campaign, LineItem
import json


def test_get_campaigns(client, test_db):
    test_campaign_1 = Campaign(name="test campaign 1")
    test_campaign_2 = Campaign(name="test campaign 2")
    test_db.add(test_campaign_1)
    test_db.add(test_campaign_2)
    test_db.commit()

    response = client.get("/api/invoices/campaigns")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "test campaign 1",
            "is_reviewed": False,
            "total_billable_amount": 0,
        },
        {
            "id": 2,
            "name": "test campaign 2",
            "is_reviewed": False,
            "total_billable_amount": 0,
        },
    ]


def test_get_campaign_single(client, test_db):
    test_campaign_1 = Campaign(name="test campaign 1")
    test_db.add(test_campaign_1)
    test_db.commit()

    response = client.get(f"/api/invoices/campaigns/{test_campaign_1.id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": test_campaign_1.id,
        "name": "test campaign 1",
        "is_reviewed": False,
        "total_billable_amount": 0,
    }


def test_get_line_items(client, test_db, requests_mock):
    requests_mock.get(
        "http://data.fixer.io/api/latest",
        text=json.dumps(
            {
                "success": True,
                "timestamp": 1690483203,
                "base": "EUR",
                "date": "2023-07-27",
                "rates": {"GBP": 0.857228, "JPY": 153.200558, "EUR": 1, "USD": 2},
            }
        ),
    )

    test_campaign_1 = Campaign(name="test campaign 1")
    test_db.add(test_campaign_1)
    test_db.flush()

    test_line_item_1 = LineItem(
        name="test line item 1",
        campaign_id=test_campaign_1.id,
        booked_amount=100.00,
        actual_amount=200.00,
        adjustments=-50.00,
        is_reviewed=False,
        is_archived=False,
    )
    test_line_item_2 = LineItem(
        name="test line item 2",
        campaign_id=test_campaign_1.id,
        booked_amount=700.00,
        actual_amount=300.00,
        adjustments=100.00,
        is_reviewed=False,
        is_archived=False,
    )

    test_db.add(test_campaign_1)
    test_db.add(test_line_item_1)
    test_db.add(test_line_item_2)
    test_db.commit()

    response = client.get(f"/api/invoices/line-items?campaign_id={test_campaign_1.id}")
    assert response.status_code == 200
    resp_data = response.json()

    assert resp_data == [
        {
            "id": test_line_item_1.id,
            "name": "test line item 1",
            "campaign_id": test_campaign_1.id,
            "booked_amount": 100.00,
            "actual_amount": 200.00,
            "adjustments": -50.00,
            "billable_amount": 150.00,
            "billable_amount_euro": 75.00,
            "is_reviewed": False,
            "is_archived": False,
            "campaign": {
                "id": test_campaign_1.id,
                "is_reviewed": False,
                "name": "test campaign 1",
                "total_billable_amount": 550.0,
            },
        },
        {
            "id": test_line_item_2.id,
            "name": "test line item 2",
            "campaign_id": test_campaign_1.id,
            "booked_amount": 700.00,
            "actual_amount": 300.00,
            "adjustments": 100.00,
            "billable_amount": 400.00,
            "billable_amount_euro": 200.00,
            "is_reviewed": False,
            "is_archived": False,
            "campaign": {
                "id": test_campaign_1.id,
                "is_reviewed": False,
                "name": "test campaign 1",
                "total_billable_amount": 550.0,
            },
        },
    ]


def test_edit_line_items_is_reviewed(client, test_db, requests_mock):
    requests_mock.get(
        "http://data.fixer.io/api/latest",
        text=json.dumps(
            {
                "success": True,
                "timestamp": 1690483203,
                "base": "EUR",
                "date": "2023-07-27",
                "rates": {"GBP": 0.857228, "JPY": 153.200558, "EUR": 1, "USD": 2},
            }
        ),
    )
    test_campaign_1 = Campaign(name="test campaign 1")
    test_db.add(test_campaign_1)
    test_db.flush()

    test_line_item_1 = LineItem(
        name="test line item 1",
        campaign_id=test_campaign_1.id,
        booked_amount=100.00,
        actual_amount=200.00,
        adjustments=-50.00,
        is_reviewed=False,
        is_archived=False,
    )
    test_line_item_2 = LineItem(
        name="test line item 2",
        campaign_id=test_campaign_1.id,
        booked_amount=700.00,
        actual_amount=300.00,
        adjustments=100.00,
        is_reviewed=False,
        is_archived=False,
    )

    test_db.add(test_campaign_1)
    test_db.add(test_line_item_1)
    test_db.add(test_line_item_2)
    test_db.commit()

    test_patch_data = json.dumps(
        {
            "is_reviewed": True,
        }
    )

    response = client.patch(
        f"/api/invoices/line-items/{test_line_item_1.id}", data=test_patch_data
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_line_item_1.id,
        "name": "test line item 1",
        "campaign_id": test_campaign_1.id,
        "booked_amount": 100.00,
        "actual_amount": 200.00,
        "adjustments": -50.00,
        "billable_amount": 150.00,
        "billable_amount_euro": 75.00,
        "is_reviewed": True,
        "is_archived": False,
        "campaign": {
            "id": test_campaign_1.id,
            "is_reviewed": False,
            "name": "test campaign 1",
            "total_billable_amount": 550.0,
        },
    }


def test_edit_line_items_adjustments(client, test_db, requests_mock):
    requests_mock.get(
        "http://data.fixer.io/api/latest",
        text=json.dumps(
            {
                "success": True,
                "timestamp": 1690483203,
                "base": "EUR",
                "date": "2023-07-27",
                "rates": {"GBP": 0.857228, "JPY": 153.200558, "EUR": 1, "USD": 2},
            }
        ),
    )

    test_campaign_1 = Campaign(name="test campaign 1")
    test_db.add(test_campaign_1)
    test_db.flush()

    test_line_item_1 = LineItem(
        name="test line item 1",
        campaign_id=test_campaign_1.id,
        booked_amount=100.00,
        actual_amount=200.00,
        adjustments=-50.00,
        is_reviewed=False,
        is_archived=False,
    )
    test_line_item_2 = LineItem(
        name="test line item 2",
        campaign_id=test_campaign_1.id,
        booked_amount=700.00,
        actual_amount=300.00,
        adjustments=100.00,
        is_reviewed=False,
        is_archived=False,
    )

    test_db.add(test_campaign_1)
    test_db.add(test_line_item_1)
    test_db.add(test_line_item_2)
    test_db.commit()

    test_patch_data = json.dumps(
        {
            "adjustments": 2000.00,
        }
    )

    response = client.patch(
        f"/api/invoices/line-items/{test_line_item_1.id}", data=test_patch_data
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_line_item_1.id,
        "name": "test line item 1",
        "campaign_id": test_campaign_1.id,
        "booked_amount": 100.00,
        "actual_amount": 200.00,
        "adjustments": 2000.00,
        "billable_amount": 2200.00,
        "billable_amount_euro": 1100.00,
        "is_reviewed": False,
        "is_archived": False,
        "campaign": {
            "id": test_campaign_1.id,
            "is_reviewed": False,
            "name": "test campaign 1",
            "total_billable_amount": 2600.0,
        },
    }


def test_edit_line_items_reviewed(client, test_db):
    test_campaign_1 = Campaign(name="test campaign 1")
    test_db.add(test_campaign_1)
    test_db.flush()

    test_line_item_1 = LineItem(
        name="test line item 1",
        campaign_id=test_campaign_1.id,
        booked_amount=100.00,
        actual_amount=200.00,
        adjustments=-50.00,
        is_reviewed=True,
        is_archived=False,
    )
    test_line_item_2 = LineItem(
        name="test line item 2",
        campaign_id=test_campaign_1.id,
        booked_amount=700.00,
        actual_amount=300.00,
        adjustments=100.00,
        is_reviewed=False,
        is_archived=False,
    )

    test_db.add(test_campaign_1)
    test_db.add(test_line_item_1)
    test_db.add(test_line_item_2)
    test_db.commit()

    test_patch_data = json.dumps(
        {
            "name": "New Name",
        }
    )

    response = client.patch(
        f"/api/invoices/line-items/{test_line_item_1.id}", data=test_patch_data
    )
    assert response.status_code == 400
