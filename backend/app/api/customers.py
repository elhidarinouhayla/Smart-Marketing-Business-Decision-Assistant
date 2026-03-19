from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.customer import Customer
from backend.app.schemas.customer import CustomerCreate, CustomerResponse
from backend.app.authentification.auth import verify_token
from sklearn.cluster import KMeans
from typing import List
import numpy as np

router = APIRouter(prefix="/customers", tags=["Customers"])


# lister tous les clients 
@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    return db.query(Customer).all()




# ajouter un client 
@router.post("/", response_model=CustomerResponse)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    new_customer = Customer(age=data.age, income=data.income)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer



# lancer le clustering KMeans 
@router.post("/clustering")
def run_clustering(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    customers = db.query(Customer).all()

    if len(customers) < 3:
        raise HTTPException(status_code=400, detail="Il faut au moins 3 clients pour lancer le clustering")

    data = np.array([[c.age, c.income] for c in customers])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(data)

    segment_names = {
    0: "Low_Engagement",
    1: "High_Income_Senior",
    2: "High_Spender_Female",
    3: "Engaged_Clicker"
}

    for i, customer in enumerate(customers):
        customer.segment_label = segment_names[labels[i]]

    db.commit()

    return {"message": f"Clustering terminé sur {len(customers)} clients", "segments": segment_names}



# voir les segments avec statistiques
@router.get("/segments")
def get_segments(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    customers = db.query(Customer).all()

    segments = {}
    for c in customers:
        label = c.segment_label or "Non segmenté"
        segments[label] = segments.get(label, 0) + 1

    return {"segments": segments}