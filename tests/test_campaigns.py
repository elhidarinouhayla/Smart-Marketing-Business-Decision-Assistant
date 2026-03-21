import pytest

@pytest.mark.asyncio
async def test_creer_campagne_simple(client, badge_acces):
    nouvelle_campagne = {
        "name": "Vente Flash",
        "budget": 1000,
        "channel": "Email",
        "status": "Active"
    }
    
    reponse = await client.post("/api/campaigns/", json=nouvelle_campagne, headers=badge_acces)

    assert reponse.status_code == 200
    assert reponse.json()["name"] == "Vente Flash"
    assert "id" in reponse.json() 