from fastapi import APIRouter
from ..models.user import User

router: APIRouter = APIRouter()

@router.post(path="/signup")
async def signup_handler(user: User):
    added_user: User = user.add()
    if type(added_user) is User:
        return added_user

@router.get(path="/auth")
async def auth_handler():
    return {"user": "authenticated"}