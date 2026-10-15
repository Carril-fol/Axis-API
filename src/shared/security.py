from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()


def hash_password(plain: str) -> str:
    return ph.hash(plain)


def verify_password(hashed: str, plain: str) -> bool:
    try:
        ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False
    return True
