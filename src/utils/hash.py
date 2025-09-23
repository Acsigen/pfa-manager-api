import hashlib
import os

def hash_password(password: str):
    salt = os.getenv("PFA_SECRET_KEY")
    data_salting = salt.encode() + password.encode()
    hash_object = hashlib.sha256(data_salting)
    hex_digest = hash_object.hexdigest()
    return hex_digest