import pytest

@pytest.fixture
async def id_campagne_reco(client, badge_acces):
    res = await client.post("/api/campaigns/", json={"name": "Test Reco", "budget": 1000, "channel": "Email", "status": "Active"}, headers=badge_acces)
    return res.json()["id"]

@pytest.mark.asyncio
async def test_generer_recommandation(client, badge_acces, id_campagne_reco):
    donnees_entree = {
        "campaign_id": id_campagne_reco,
        "probability": 0.85,
        "prediction": 1
    }

    reponse = await client.post("/api/recommendations/generate", json=donnees_entree, headers=badge_acces)

  
    assert reponse.status_code == 200
    
    data = reponse.json()
    assert "advice_text" in data 
    assert data["campaign_id"] == id_campagne_reco
    assert "id" in data