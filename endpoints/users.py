from datetime import datetime
from argon2 import PasswordHasher
from fastapi.security.api_key import APIKey


from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette import status
from auth import get_jwt

from database import *
from fastapi.encoders import jsonable_encoder
import jwt

router = APIRouter()


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str
    password: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Louis Le Gatt",
                "email": "test@truc.bidule",
                "password": "this is a bidule",
            }
        }


@router.get("/users/")
async def getAllUsers(token : APIKey = Depends(get_jwt)):
    users = await db["users"].find().to_list(50)
    return users

class Login(BaseModel):
    email: str
    password: str

@router.post("/users/login")
async def Loggin(login: Login = Body(...)):
    login = jsonable_encoder(login)
    user = await db["users"].find_one({'email': login["email"]})

    if not user:
        raise HTTPException(status_code=403, detail="Wrong Email or Password")
    
    try: 
        PasswordHasher().verify(user["password"], login["password"])
    except:
        raise HTTPException(status_code=403, detail="Wrong Email or Password")
    
    token = jwt.encode(
        {
            "userId" : user["_id"],
            "userName" : user["name"],
        },
        "secret",
        algorithm="HS512"
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content=token)
    



@router.post("/users/register")
async def AddUser(user: User = Body(...)):
    user = jsonable_encoder(user)
    print(user)
    userDoesExist = await db["users"].find_one({'email': user["email"]})

    if userDoesExist :
        raise HTTPException(status_code=403, detail="This accout already exists")
    
    user["password"] = PasswordHasher().hash(user["password"])


    newUser = await db["users"].insert_one(user)
    created = await db["users"].find_one({"_id": newUser.inserted_id})

    token = jwt.encode(
        {
            "userId" : created["_id"],
            "userName" : created["name"],
        },
        "secret",
        algorithm="HS512"
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=token)
