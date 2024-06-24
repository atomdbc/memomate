from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/entries/", response_model=schemas.Entry)
def create_entry(entry: schemas.Entry, db: Session = Depends(get_db)):
    return crud.create_entry(db=db, entry=entry)

@router.get("/entries/{user_id}", response_model=list[schemas.Entry])
def read_entries(user_id: int, db: Session = Depends(get_db)):
    return crud.get_entries(db=db, user_id=user_id)
