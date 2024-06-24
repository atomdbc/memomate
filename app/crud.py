from sqlalchemy.orm import Session
from app import models, schemas

def create_entry(db: Session, entry: schemas.Entry):
    db_entry = models.JournalEntry(user_id=entry.user_id, content=entry.content)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_entries(db: Session, user_id: int):
    return db.query(models.JournalEntry).filter(models.JournalEntry.user_id == user_id).all()
