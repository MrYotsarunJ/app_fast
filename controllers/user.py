from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import EmailStr
from enum import Enum

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

class StatusEnum(str, Enum):
    request = "request"
    approved = "approved"
    rejected = "rejected"


async def user_dto(
        q:str|None = None, 
        page:int = 1,
        email:EmailStr|None = None,
        status:StatusEnum = StatusEnum.request
):
    return {
        "q":q,
        "page":page,
        "email":email,
        "status":status
    }


@user_router.get("/list")
async def list_user(
    params: Annotated[dict, Depends(user_dto)]
):
    
    return {
            "query_string": params,
            "data":[
            {"id":1, "username":"user1", "email":"user1@test.com"},
            {"id":2, "username":"user2", "email":"user2@test.com"},
            {"id":3, "username":"user3", "email":"user3@test.com"},
        ]
    }