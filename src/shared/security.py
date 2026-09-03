from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Hashing costs ~76ms of CPU, so it is kept out of the pydantic validators and
# called from the services, where it is explicit and skippable.
ph = PasswordHasher()


def hash_password(plain: str) -> str:
    return ph.hash(plain)


def verify_password(hashed: str, plain: str) -> bool:
    try:
        ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False
    return True
