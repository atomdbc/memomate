from sqlalchemy import Column, Integer, Text
from app.database import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    content = Column(Text, index=True)
