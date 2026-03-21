import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.db.database import Base, engine, get_db
from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.authentification.auth import hache_password

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    
    admin = session.query(User).filter(User.username == "admin").first()
    if not admin:
        hashed_pwd = hache_password("123")
        new_user = User(username="admin", password=hashed_pwd, email="admin@test.com")
        session.add(new_user)
        session.commit()
    
    yield session
    session.close()

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def badge_acces(client):
    res = await client.post("/api/auth/login", json={"username": "admin", "password": "123"})
    if res.status_code != 200:
        await client.post("/api/auth/register", json={"username": "admin", "password": "123", "email": "admin@test.com"})
        res = await client.post("/api/auth/login", json={"username": "admin", "password": "123"})
    
    token = res.json()["token"]
    return {"token": token}

@pytest.fixture
async def auth_headers(badge_acces):
    return badge_acces
