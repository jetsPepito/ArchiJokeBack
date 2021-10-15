from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette import status

from database import *
from fastapi.encoders import jsonable_encoder

router = APIRouter()


class Joke(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    body: str
    date: datetime
    likes: int
    dislikes: int
    author: str
    author_id: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Une bonne blague",
                "body": "Sah quel plaisir",
                "date": "2021-09-01T22:00:00.000Z",
                "likes": 12,
                "dislikes": 5,
                "author": "Louis"
            }
        }


@router.get("/jokes")
async def getAllJokes():
    jokes = await db["jokes"].find().to_list(50)
    return jokes


@router.post("/jokes")
async def addJoke(joke: Joke = Body(...)):
    joke = jsonable_encoder(joke)
    newJoke = await db["jokes"].insert_one(joke)
    created = await db["jokes"].find_one({"_id": newJoke.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created)
