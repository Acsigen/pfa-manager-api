from fastapi import APIRouter, Depends
from ..models.user import User, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from ..utils.jwt import create_access_token, validate_token
from datetime import timedelta

router: APIRouter = APIRouter(tags=["auth"])


@router.post(path="/signup", status_code=201)
async def signup_handler(user: User):
    added_user: User = user.add()
    if type(added_user) is User:
        return added_user


@router.post(path="/auth", status_code=200)
async def auth_handler(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    authenticated_user_id: int = authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if type(authenticated_user_id) is int:
        access_token = create_access_token(
            username=form_data.username,
            user_id=authenticated_user_id,
            expires_delta=timedelta(minutes=60),
        )
        return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    token: Annotated[str, Depends(dependency=OAuth2PasswordBearer(tokenUrl="auth"))],
):
    current_user: dict = validate_token(token=token)
    return current_user
