from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI()

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PlaceDB(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    description = Column(String, nullable=True)
    coffee = Column(Boolean)
    wifi = Column(Boolean)
    food = Column(Boolean)
    lat = Column(Float)
    long = Column(Float)
    
Base.metadata.create_all(bind=engine)

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
        
def create_place(db: Session, place: Place):
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

@app.post('/places/', response_model=Place)
async def create_new_place(place: Place, db: Session = Depends(get_db)):
    db_place = create_place(db, place)
    return db_place

@app.get('/places/', response_model=List[Place])
async def read_places(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    places = get_places(db, skip, limit)
    return places

@app.get('/places/{place_id}', response_model=Place)
async def read_place(place_id: int, db: Session = Depends(get_db)):
    place = get_place(db, place_id)
    return place

@app.get('/')
async def read_root():
    return {'message': 'Hello World'}
