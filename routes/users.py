from fastapi import APIRouter, Response, status, HTTPException
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User, UserPost
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import *

users = APIRouter()


@users.get('/users', response_model=list[User], tags=["users"])
async def find_all_users():
    return usersEntity(conn.local.user.find())


@users.post('/users', response_model=UserPost, tags=["users"])
async def create_user(user: UserPost):
    new_user = dict(user)
    # del (new_user['id'])
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])

    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({"_id": id})

    return userEntity(user)


@users.get('/users/{id}', response_model=User, tags=["users"])
async def find_user_by_id(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@users.put('/users/{id}', response_model=User, tags=["users"])
async def update_user(id: str, user: User):
    updated_user = conn.local.user.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@users.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):

    result = userEntity(
        conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))

    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=HTTP_204_NO_CONTENT)
