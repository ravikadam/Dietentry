# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from datetime import datetime
from typing import List, Any


DATABASE_URL = "postgresql://doadmin:AVNS_bMGFjnoQzyxk96lM7wH@ravipost-do-user-721507-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    age = Column(Integer)
    weight = Column(Float)
    user_data = relationship("UserData", back_populates="user")
    recommendations = relationship("UserRecommendation", back_populates="user")

class UserData(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    food = Column(String)
    calories_burnt = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="user_data")

class UserRecommendation(Base):
    __tablename__ = "user_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recommendation = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="recommendations")

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    age: int
    weight: float

class UserDataCreate(BaseModel):
    user_id: int
    food: str
    calories_burnt: float

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/user_data/")
def create_user_data(data: UserDataCreate, db: Session = Depends(SessionLocal)):
    db_data = UserData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@app.get("/recommendation/{user_id}")
def get_recommendation(user_id: int, db: Session = Depends(SessionLocal)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Simple recommendation logic based on user's weight
    if user.weight < 60:
        recommendation = "Eat more protein-rich foods"
    elif 60 <= user.weight < 80:
        recommendation = "Maintain a balanced diet"
    else:
        recommendation = "Consider a low-carb diet"

    # Save the recommendation to the database
    db_recommendation = UserRecommendation(user_id=user_id, recommendation=recommendation)
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)

    return {"recommendation": recommendation, "date": db_recommendation.date}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
