from pydantic import BaseModel


# schema pydantic creation du user
class UserCreate(BaseModel):
    username : str
    password : str
    email : str


class UserVerify(BaseModel):
    username : str
    password : str


class UserResponse(UserCreate):
    id : int