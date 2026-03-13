from jose import jwt
from fastapi import HTTPException, Header
from ..config import SECRET_KEY, ALGORITHM
from passlib.context import CryptContext


def create_token(username:str, user_id: int):
    paylod = {
        "sub": username,
        "id" : user_id
        }
    token = jwt.encode(paylod,SECRET_KEY,algorithm=ALGORITHM)
    return token


def verify_token(token: str = Header(...)):
    try:
        paylod = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        return paylod
    except:
        raise HTTPException(status_code=400, detail="le token est invalide")
    


password_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hache_password(password):
    return password_context.hash(password)

def verify_password(password,hash_password):
    return password_context.verify(password,hash_password)
    