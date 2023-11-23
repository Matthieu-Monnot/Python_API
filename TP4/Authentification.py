from __future__ import annotations
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

available_subscriptions = ["free", "premium", "company"]

def load_users_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_users_to_json(users, file_path):
    with open(file_path, 'w') as f:
        json.dump(users, f, indent=2)


file_path = "db_users.json"
fake_users_db = load_users_from_json(file_path)




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
    abonement: str = None


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


async def get_access_moneyflowclassique(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.abonement != "free":
        raise HTTPException(status_code=400, detail="Function available only for free subscription")
    return current_user


async def get_access_rsi(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.abonement != "premium":
        raise HTTPException(status_code=400, detail="Function available only for premium subscription")
    return current_user

async def get_access_macd(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.abonement != "company":
        raise HTTPException(status_code=400, detail="Function available only for company subscription")
    return current_user

async def get_access_sma(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.abonement != "company" and current_user.abonement != "premium":
        raise HTTPException(status_code=400, detail="Function available only for company subscription and premium subscription")
    return current_user

def update_user_subscription(current_user, new_subscription):
    if new_subscription not in available_subscriptions:
        raise HTTPException(status_code=400, detail="Invalide parameters, please enter 'free' or 'premium' or 'company'")

    if current_user.username in fake_users_db:
        fake_users_db[current_user.username]["abonement"] = new_subscription
        save_users_to_json(fake_users_db, file_path)
        current_user.abonement = new_subscription
        return current_user
    return None


def save_new_user(username, password, full_name, email, abonement):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username is already taken")

    hashed_password = fake_hash_password(password)
    new_user = {
        "username": username,
        "full_name": full_name,
        "email": email,
        "hashed_password": hashed_password,
        "abonement":abonement,
    }

    fake_users_db[username] = new_user
    save_users_to_json(fake_users_db, file_path)
    return {"message": "User successfully registered"}


def delete_user(username, current_user):
    if username not in fake_users_db:
        raise HTTPException(status_code=400, detail="User not found")

    if username != current_user.username:
        raise HTTPException(status_code=400, detail="You cannot delete an other account")

    del fake_users_db[username]
    save_users_to_json(fake_users_db, file_path)
    return {"message": "User successfully deleted"}
