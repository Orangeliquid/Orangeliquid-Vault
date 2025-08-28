import os
import bcrypt
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

SECRET_FILE = ".secret_key"


def hash_password(password: str) -> bytes:
    """
    password.encode() converts the string password to bytes (required by bcrypt).
    bcrypt.gensalt() generates a random salt.
    bcrypt.hashpw() takes the password bytes + salt and returns a hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """
    password.encode() converts the input password to bytes.
    bcrypt.checkpw() hashes the input password with the salt stored inside the hashed password,
    then compares the result with the stored hash.
    """
    return bcrypt.checkpw(password.encode(), hashed)


def save_master_password_hash(hashed: bytes) -> None:
    """
    Opens SECRET_FILE and writes the hashed master password passed to function.
    """
    with open(SECRET_FILE, "wb") as f:
        f.write(hashed)


def load_master_password_hash() -> bytes | None:
    """
    Reads the hashed master password from SECRET_FILE.
    Return None if the file does not exist.
    """
    if not os.path.exists(SECRET_FILE):
        return None
    with open(SECRET_FILE, "rb") as f:
        return f.read()


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive an encryption key from the password and salt passed using PBKDF2.
    Returns base64-encoded bytes suitable for Fernet or similar libraries.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )

    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


# If .vault_salt is deleted -> encrypted data will be lost
def get_or_create_salt() -> bytes:
    """
    Ensure persistent salt for key derivation.
    """
    salt_file = ".vault_salt"
    if os.path.exists(salt_file):
        with open(salt_file, "rb") as f:
            return f.read()

    salt = os.urandom(16)
    with open(salt_file, "wb") as f:
        f.write(salt)
    return salt
