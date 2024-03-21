from pydantic import BaseModel
import datetime
from typing import Optional

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime
    
    
class request_user(BaseModel):
    email: str
    password: str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    
class change_password(BaseModel):
    email: str
    old_password: str
    new_password: str
    
class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status:bool
    created_at: datetime.datetime    
    
class Place(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    coffee: bool
    wifi: bool
    food: bool
    lat: float
    long: float
     
    class Config:
        orm_mode = True    