import pytest

@pytest.fixture
async def preparer_3_clients(client, badge_acces):
    for i in range(3):
        await client.post("/api/customers/", json={
            "age": 20 + (i * 10), 
            "income": 30000 + (i * 5000)
        }, headers=badge_acces)
    return True

@pytest.mark.asyncio
async def test_run_clustering_success(client, badge_acces, preparer_3_clients):
    # n_clusters=2 since we have 3 clients (3 is minimum for n=3)
    # Wait, the default is 3. If I have 3 clients, it's fine.
    reponse = await client.post("/api/customers/clustering", headers=badge_acces)

    assert reponse.status_code == 200
    assert "Clustering terminé" in reponse.json()["message"]
    assert "segments" in reponse.json()