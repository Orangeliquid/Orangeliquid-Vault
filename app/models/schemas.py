from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


# Ellipses tells pydantic that this field is required
class VaultEntryCreate(BaseModel):
    service: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    password_encrypted: str = Field(..., min_length=1)
    email: Optional[str] = None
    notes: Optional[str] = None


class VaultEntryRead(VaultEntryCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

