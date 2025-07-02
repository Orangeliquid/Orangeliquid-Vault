from app.database import SessionLocal
from app.models.vault_entry import VaultEntry
from app.models.schemas import VaultEntryCreate


def create_entry(entry_data: VaultEntryCreate):
    db = SessionLocal()

    entry = VaultEntry(
        service=entry_data.service,
        username=entry_data.username,
        password_encrypted=entry_data.password_encrypted,
        email=entry_data.email,
        notes=entry_data.notes,
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
