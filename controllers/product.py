from fastapi import APIRouter
from pydantic import BaseModel, constr
from enum import Enum
from typing import Optional

product_router = APIRouter(
    prefix="/product",
    tags=["product"]
)

class StatusEnum(str, Enum):
    request = "request"
    approved = "approved"
    rejected = "rejected"

class Item(BaseModel):
    name: constr(strip_whitespace=True)
    price: float
    status:StatusEnum = StatusEnum.request
    description:Optional[str] = None

@product_router.post("/items")
async def create_item(
    product_data:Item
):
    return {
        "name": product_data.name,
        "price": product_data.price,
        "status": product_data.status,
        "description":product_data.description
    }