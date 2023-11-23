from __future__ import annotations
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Users database with 2 regular users and 1 administrator
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "admin",
        "email": "admin@fastApi.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
        "admin": True,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
        "admin": False,
    },
    "bod": {
        "username": "bod",
        "full_name": "bod Wonderson",
        "email": "bod@example.com",
        "hashed_password": "fakehashedsecret1",
        "disabled": False,
        "admin": False,
    },
}


def fake_hash_password(password: str):
    """
    Password hashing function.
    :param password: The input password to be hashed.
    :return: The hashed password.
    """
    return "fakehashed" + password

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic class to represent the structure of a user
class User(BaseModel):
    username: str
    email: str  = None
    full_name: str = None
    disabled: bool = None
    admin: bool = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    """
    Get user from the database.
    :param db: The user database.
    :param username: The username of the user to retrieve.
    :return: An instance of UserInDB if the user exists, otherwise None.
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    """
    function to decode a token.
    :param token: The token to be decoded.
    :return: An instance of UserInDB if the user exists, otherwise None.
    """
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Get the current user based on the provided token.
    :param token: The OAuth2 token.
    :return: An instance of UserInDB if the user exists, otherwise raise HTTPException.
    """
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the current active user based on the current user.
    :param current_user: The current user.
    :return: The current user if active, otherwise raise HTTPException.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Function not available because you are an Inactive user")
    return current_user


async def get_current_admin_user(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the current admin user based on the current user.
    :param current_user: The current user.
    :return:The current user if an admin, otherwise raise HTTPException.
    """
    if not current_user.admin:
        raise HTTPException(status_code=400, detail="Function not available because you are not an Administrator user")
    return current_user
