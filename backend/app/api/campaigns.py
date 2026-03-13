from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.db.database import get_db
from backend.app.models.campaign import Campaign
from backend.app.schemas.schemas import CampaignCreate, CampaignUpdate, CampaignResponse
from backend.app.authentification.auth import verify_token
from typing import List

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


# lister les campagnes de l'utilisateur connecte
@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    return db.query(Campaign).filter(Campaign.user_id == user["id"]).all()


# detail d'une campagne
@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: str, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.user_id == user["id"]).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")
    return campaign



# creer une campagne 
@router.post("/", response_model=CampaignResponse)
def create_campaign(data: CampaignCreate, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    new_campaign = Campaign(
        name=data.name,
        budget=data.budget,
        channel=data.channel,
        status=data.status,
        user_id=user["id"]
    )
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign



#  modifier une campagne 
@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: str, data: CampaignUpdate, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.user_id == user["id"]).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")

    if data.name is not None:    campaign.name = data.name
    if data.budget is not None:  campaign.budget = data.budget
    if data.channel is not None: campaign.channel = data.channel
    if data.status is not None:  campaign.status = data.status

    db.commit()
    db.refresh(campaign)
    return campaign



# supprimer une campagne 
@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: str, db: Session = Depends(get_db), user: dict = Depends(verify_token)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id, Campaign.user_id == user["id"]).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")
    db.delete(campaign)
    db.commit()
    return {"message": "Campagne supprimée"}