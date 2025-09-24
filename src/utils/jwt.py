from jose import jwt, JWTError
from os import getenv
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException

SECRET_KEY = getenv(key="SECRET_KEY")
ALGORITHM = "HS256"

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    claims = {"sub": username, "id":user_id}
    expire = datetime.now(tz=timezone.utc) + expires_delta
    claims.update({"exp": expire})
    return jwt.encode(claims=claims,key=SECRET_KEY,algorithm=ALGORITHM)

def validate_token(token):
    try:
        payload = jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401,detail="Could not validate credentials")
        return {"username": username, "user_id": user_id}
    except JWTError:
        raise HTTPException(status_code=401,detail="Could not validate credentials")