from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(email: str, db: Session = Depends(get_db)):
    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

@router.post("/login")
def login(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return {"exists": bool(user), "user": user}
