from cryptography.fernet import Fernet


def decrypt_entry(entry, fernet: Fernet):
    return {
        "service": fernet.decrypt(entry.service.encode()).decode(),
        "username": fernet.decrypt(entry.username.encode()).decode(),
        "password": fernet.decrypt(entry.password_encrypted.encode()).decode(),
        "email": (
            fernet.decrypt(entry.email.encode()).decode()
            if entry.email not in [None, "None"]
            else None
        ),
        "notes": (
            fernet.decrypt(entry.notes.encode()).decode()
            if entry.notes not in [None, "None"]
            else None
        ),
        "created_at": entry.created_at,
    }


def encrypt_field(value: str, fernet: Fernet):
    return fernet.encrypt(value.encode()).decode()
