from sqlalchemy import Column, Integer, String, Float,Boolean,DateTime,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from database import Base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100),nullable=False)
    email=Column(String(100),unique=True,nullable=False)
    password = Column(String(100),nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    
    
class Token(Base):
    __tablename__ = 'tokens'
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String(450),primary_key=True)
    refresh_token = Column(String(450),nullable=False) 
    status = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now())
    
    
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
    


    