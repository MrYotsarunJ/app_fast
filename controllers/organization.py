from typing import Annotated
from fastapi import APIRouter, Depends

from dependency import get_valid_user

from sqlalchemy.orm import Session
from database import get_db
from services import organization_service

org_router = APIRouter(
    prefix="/organization",
    tags=["organization"]
)


async def org_dto(
    q:str | None = None,
    page:int = 1
):
    return {
        "q":q,
        "page":page
    }


@org_router.get("/list")
async def list_organization(
    params: Annotated[dict, Depends(org_dto)],
    db:Session = Depends(get_db),
    user: Annotated[dict, Depends(get_valid_user)] = None,
    
):
    
    out_list = await organization_service.list_organization(db, params)

    return {
        "query_string": params,
        "user": user,
        "data": out_list
    }

