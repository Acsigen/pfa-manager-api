import os
import hashlib
import base64
import secrets

"""
Secure password hashing (stdlib only).

Produces strings of the form:
  pbkdf2_sha256$<iterations>$<salt_b64>$<dk_b64>

Functions:
 - hash_password(password, iterations=200_000) -> stored_string
 - verify_password(password, stored_string) -> bool
"""


# Tune iterations to your environment. Higher is slower but more resistant to brute force.
DEFAULT_ITERATIONS = 200_000
SALT_LEN: int = 16  # bytes
DK_LEN: int = 32  # bytes (256-bit)


def _b64(x: bytes) -> str:
    return base64.urlsafe_b64encode(s=x).rstrip(b"=").decode(encoding="ascii")


def _b64decode(s: str) -> bytes:
    # pad base64 string if needed
    padding = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s=s + padding)


def hash_password(password: str, iterations: int = DEFAULT_ITERATIONS) -> str:
    """
    Hash a password for storage.
    Returns a single string you can store in your DB.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a str")
    salt: bytes = os.urandom(SALT_LEN)
    dk: bytes = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(encoding="utf-8"),
        salt=salt,
        iterations=iterations,
        dklen=DK_LEN,
    )
    return f"pbkdf2_sha256${iterations}${_b64(x=salt)}${_b64(x=dk)}"


def verify_password(password: str, stored: str) -> bool:
    """
    Verify a password against the stored hash.
    Returns True if it matches, False otherwise.
    """
    try:
        algo, iter_s, salt_b64, dk_b64 = stored.split("$")
    except ValueError:
        return False

    if algo != "pbkdf2_sha256":
        # Unknown format / algorithm
        return False

    try:
        iterations: int = int(iter_s)
    except ValueError:
        return False

    salt: bytes = _b64decode(s=salt_b64)
    expected: bytes = _b64decode(s=dk_b64)

    new_dk: bytes = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(encoding="utf-8"),
        salt=salt,
        iterations=iterations,
        dklen=len(expected),
    )
    # Use constant-time comparison
    return secrets.compare_digest(new_dk, expected)
