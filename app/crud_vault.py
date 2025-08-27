from app.database import SessionLocal
from app.models.vault_entry import VaultEntry
from app.models.schemas import VaultEntryCreate, VaultEntryUpdate


def create_entry(entry_data: VaultEntryCreate):
    db = SessionLocal()

    entry = VaultEntry(
        service=entry_data.service,
        username=entry_data.username,
        password_encrypted=entry_data.password_encrypted,
        email=entry_data.email,
        notes=entry_data.notes,
        strength_rating=entry_data.strength_rating,
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)
    db.close()
    return entry


def get_all_entries():
    db = SessionLocal()
    entries = db.query(VaultEntry).order_by(VaultEntry.created_at.desc()).all()
    db.close()
    return entries


def update_entry(entry_id: int, update_data: VaultEntryUpdate):
    db = SessionLocal()
    try:
        entry = db.query(VaultEntry).filter(VaultEntry.id == entry_id).first()
        if entry is None:
            return None

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)

        db.commit()
        db.refresh(entry)
        return entry

    finally:
        db.close()
