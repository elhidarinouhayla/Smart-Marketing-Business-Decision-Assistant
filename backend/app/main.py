from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db.database import Base, engine
from backend.app.api.api_auth import router as auth_router
from backend.app.api.campaigns import router as campaigns_router
from backend.app.api.customers import router as customers_router
from backend.app.api.predictions import router as predictions_router
from backend.app.api.recommendations import router as recommendations_router
from backend.app.api.dashboard import router as dashboard_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Marketing Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,            prefix="/api")
app.include_router(campaigns_router,       prefix="/api")
app.include_router(customers_router,       prefix="/api")
app.include_router(predictions_router,     prefix="/api")
app.include_router(recommendations_router, prefix="/api")
app.include_router(dashboard_router,       prefix="/api")


@app.get("/")
def root():
    return {"message": "Smart Marketing API is running "}