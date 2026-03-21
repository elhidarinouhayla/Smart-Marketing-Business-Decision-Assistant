import pytest


@pytest.fixture
async def id_campagne(client, auth_headers):
    res = await client.post("/api/campaigns/", json={"name": "Promo", "budget": 500, "channel": "Social Media", "status": "Active"}, headers=auth_headers)
    return res.json()["id"]


@pytest.mark.asyncio
async def test_prediction(client, auth_headers, id_campagne):
 
    donnees = {
        "campaign_id": id_campagne,
        "Age": 25,
        "Income": 50000.0,
        "WebsiteVisits": 10,
        "SocialShares": 5,
        "Gender": "Male",
        "CampaignChannel": "Email",
        "CampaignType": "Promotion",
        "AdvertisingPlatform": "Google Ads",
        "AdvertisingTool": "Search",
        "SegmentName": "High_Income_Senior",
        "AdSpend": 100.0,
        "ClickThroughRate": 0.05,
        "PagesPerVisit": 2.5,
        "TimeOnSite": 120.0,
        "EmailOpens": 2,
        "EmailClicks": 1,
        "PreviousPurchases": 3,
        "LoyaltyPoints": 150
    }
    
    reponse = await client.post("/api/predictions/", json=donnees, headers=auth_headers)

    assert reponse.status_code == 200
    assert "message" in reponse.json()