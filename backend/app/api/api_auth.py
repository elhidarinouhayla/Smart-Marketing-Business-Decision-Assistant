from fastapi import APIRouter,HTTPException,Depends 
from backend.app.db.database import Base,engine,get_db
from sqlalchemy.orm import session
from backend.app.schemas.user_schema import UserCreate, UserResponse,  UserVerify
from backend.app.models.user import User
from backend.app.authentification.auth import create_token, hache_password, verify_password
from fastapi.middleware.cors import CORSMiddleware




router = APIRouter(prefix="/auth", tags=["Auth"])
Base.metadata.create_all(bind=engine)



# creation d'un username :
@router.post("/register", response_model=UserResponse)
def create_user(user:UserCreate, db: session=Depends(get_db)):
    exist = db.query(User).filter(User.username == user.username).first()

    if exist:
        raise HTTPException(status_code=400, detail= "username existe deja")
    
    # haching password
    hashed_pwd = hache_password(user.password)
    
    new_user = User(username=user.username, password=hashed_pwd, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# verifier l'identifiant et encoder token
@router.post("/login")
def login(user:UserVerify, db: session=Depends(get_db)):

    db_user = db.query(User).filter(
        User.username == user.username
        ).first()
    
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400, detail="username or password incorect")
    
    token = create_token(db_user.username, user_id=db_user.id)

    return {"token" : token, "username": db_user.username}






