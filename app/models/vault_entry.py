from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()


class VaultEntry(Base):
    __tablename__ = "vault"

    id = Column(Integer, primary_key=True)
    service = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_encrypted = Column(String, nullable=False)
    email = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    strength_rating = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
