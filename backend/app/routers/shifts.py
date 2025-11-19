from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.db import SessionLocal
from app.models.shift import Shift, ShiftStatus
from uuid import UUID

router = APIRouter(prefix="/shifts", tags=["Shifts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/start")
def start_shift(user_id: UUID, db: Session = Depends(get_db)):
    # check if there's a running shift for user
    running = db.query(Shift).filter(Shift.user_id == user_id, Shift.status == ShiftStatus.running).first()
    if running:
        raise HTTPException(status_code=400, detail="A shift is already running for this user")
    shift = Shift(user_id=user_id, start_time=datetime.utcnow(), status=ShiftStatus.running)
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift

@router.post("/{shift_id}/stop")
def stop_shift(shift_id: UUID, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    if shift.status == ShiftStatus.stopped:
        raise HTTPException(status_code=400, detail="Shift already stopped")
    shift.end_time = datetime.now(timezone.utc)
    diff = shift.end_time - shift.start_time
    shift.duration = timedelta(seconds=diff.total_seconds())
    shift.status = ShiftStatus.stopped
    db.commit()
    db.refresh(shift)
    return shift

@router.get("/user/{user_id}")
def list_user_shifts(user_id: UUID, db: Session = Depends(get_db)):
    shifts = db.query(Shift).filter(Shift.user_id == user_id).order_by(Shift.start_time.desc()).all()
    return shifts

@router.get("/{shift_id}")
def get_shift(shift_id: UUID, db: Session = Depends(get_db)):
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    return shift
