from database import Base,engine,SessionLocal,Session
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from auth_bearer import JWTBearer
from functools import wraps
from models import UserModel, Token,PlaceDB
import schemas 
from utils import get_hashed_password, verify_password,create_access_token,create_refresh_token
from typing import List


JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_REFRESH_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


app = FastAPI()
# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
def create_place(db: Session, place: schemas.Place):
    db_place = PlaceDB(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

def get_place(db: Session, place_id: int):
    place = db.query(PlaceDB).filter(PlaceDB.id == place_id).first()
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return place

def get_places(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PlaceDB).offset(skip).limit(limit).all()

@app.post('/places/', response_model=schemas.Place)
async def create_new_place(place: schemas.Place, db: Session = Depends(get_db)):
    db_place = create_place(db, place)
    return db_place

@app.get('/places/', response_model=List[schemas.Place])
async def read_places(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    places = get_places(db, skip, limit)
    return places

@app.get('/places/{place_id}', response_model=schemas.Place)
async def read_place(place_id: int, db: Session = Depends(get_db)):
    place = get_place(db, place_id)
    return place

@app.get('/')
async def read_root():
    return {'message': 'Hello World'}

# user registration

@app.post('/register', response_model=schemas.User)
def register_user(user: schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    encrypted_password = get_hashed_password.hash(user.password)
    new_user = UserModel(
        username = user.username,
        email = user.email,
        password = encrypted_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
            "data": new_user,
            "message": "User created successfully"
            }

# user login
@app.post('/login')
def login(request:schemas.request_user, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.email == request.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email provided ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hash_password = user.password
    if not verify_password(request.password, hash_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password provided ",
            headers={"WWW-Authenticate": "Bearer"},
        )    
    access =create_access_token(user.id)
    refresh=create_refresh_token(user.id)
    
    token_db = Token(
        user_id = user.id,
        access_token = access,
        refresh_token = refresh,
        status = True
    )
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh
    }
    
# get user
@app.get('/user', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# get all users
@app.get('/users', response_model=List[schemas.User])
def get_users(dependencies=Depends(JWTBearer()), db: Session = Depends(get_db)):
    users = db.query(schemas.User).all()
    return users