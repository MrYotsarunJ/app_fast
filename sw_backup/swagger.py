from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from dependency import get_valid_user

swagger_router = APIRouter(prefix="/swagger", tags=["Swagger (Demo)"])

# Mock database
user_db = {
    1: {"username": "alice", "email": "alice@example.com"},
    2: {"username": "bob", "email": "bob@example.com"},
}


# User DTO
class User(BaseModel):
    username: str
    email: EmailStr


# 🔵 GET all users
@swagger_router.get(
    "/", summary="ดึงรายการผู้ใช้ทั้งหมด", description="เรียกดูผู้ใช้ทั้งหมดจากฐานข้อมูลจำลอง"
)
def list_users(
    user: Annotated[dict, Depends(get_valid_user)] = None,
):
    return user_db


# 🔵 GET user by ID
@swagger_router.get(
    "/{user_id}",
    summary="ดึงข้อมูลผู้ใช้ตาม ID",
    description="ระบุ user_id เพื่อเรียกดูข้อมูลผู้ใช้นั้น หากไม่พบจะได้ HTTP 404",
    response_model=User,
)
def get_user(user_id: int = Path(..., gt=0, description="ID ของผู้ใช้ ต้องมากกว่า 0")):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db[user_id]


# 🟢 POST new user
@swagger_router.post(
    "/",
    summary="สร้างผู้ใช้ใหม่",
    description="รับข้อมูล username และ email เพื่อเพิ่มผู้ใช้ใหม่",
    response_model=dict,
)
def create_user(user: User):
    user_id = max(user_db.keys(), default=0) + 1
    user_db[user_id] = user.dict()
    return {"id": user_id, "user": user}


# 🟡 PUT: replace user data
@swagger_router.put(
    "/{user_id}",
    summary="แทนที่ข้อมูลผู้ใช้ทั้งหมด",
    description="ใช้สำหรับอัปเดตข้อมูลผู้ใช้แบบเต็มรูปแบบ (ต้องส่งทุก field)",
    response_model=dict,
)
def update_user(user_id: int, user: User):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_db[user_id] = user.dict()
    return {"id": user_id, "user": user}


# 🟠 PATCH: update user partially
@swagger_router.patch(
    "/{user_id}",
    summary="อัปเดตข้อมูลบางส่วนของผู้ใช้",
    description="อัปเดตบาง field เช่น username หรือ email โดยไม่ต้องส่งทั้ง object",
    response_model=dict,
)
def patch_user(
    user_id: int,
    username: Optional[str] = Query(None, description="ชื่อผู้ใช้ใหม่"),
    email: Optional[EmailStr] = Query(None, description="อีเมลใหม่"),
):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    if username:
        user_db[user_id]["username"] = username
    if email:
        user_db[user_id]["email"] = email
    return {"id": user_id, "user": user_db[user_id]}


# 🔴 DELETE: remove user
@swagger_router.delete(
    "/{user_id}",
    summary="ลบผู้ใช้ออกจากระบบ",
    description="ลบข้อมูลผู้ใช้ตาม ID หากไม่พบจะคืนค่า HTTP 404",
)
def delete_user(user_id: int):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    del user_db[user_id]
    return {"message": f"User {user_id} deleted"}
