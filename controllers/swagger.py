from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from dependency import get_valid_user

swagger_router = APIRouter(prefix="/swagger", tags=["Swagger (Demo)"])

user_db = {
    1: {"username": "alice", "email": "alice@example.com"},
    2: {"username": "bob", "email": "bob@example.com"},
    3: {"username": "test", "email": "test@example.com"},
}

# สร้างผู้ใช้ 4,5  ชื่ออะไรก็ได้
# id 1 username "sbs"
# ลบ id 2
# id 3 "username": "user3" "email": "user3@gmail.com" 


class User(BaseModel):
    username: str
    email: EmailStr


@swagger_router.get(
    "/", summary="ดึงรายการผู้ใช้", description="เรียกข้อมูลผู้ใช้ทั้งหมดจากฐานข้อมูลจำลอง"
)
def list_user(user: Annotated[dict, Depends(get_valid_user)] = None):
    return user_db


@swagger_router.get(
    "/{user_id}",
    summary="ดึงรายการผู้ใช้ ตาม ID",
    description="ระบุ user_id เพื่อเรียกดูข้อมูลผู้ใช้นั้น หากไม่พบจะคือค่าเป็น HTTP 404",
    response_model=User,
)
def get_user(user_id: int = Path(..., gt=0, description="ID ของผู้ใช้ต้องมากกว่า 0")):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not Found")

    return user_db[user_id]


@swagger_router.post(
    "/",
    summary="เพิ่มผู้ใช้ใหม่",
    description="รับข้อมูล Username และ Email เพื่อเพิ่มข้อมูล",
    response_model=dict,
)
def create_user(user: User):
    user_id = max(user_db.keys(), default=0) + 1
    user_db[user_id] = user.dict()

    return {"id": user_id, "user": user}


@swagger_router.put(
    "/{user_id}",
    summary="แทนที่ข้อมูลผู้ใช้",
    description="ใช้สำหรับการอัปเดทข้อมูลผู้ใช้แบบเต็มรูปแบบ (จำเป็นต้องส่งทุก Field)",
    response_model=dict,
)
def update_user(user_id: int, user: User):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_db[user_id] = user.dict()
    return {"id": user_id, "user": user}


@swagger_router.patch(
    "/{user_id}",
    summary="อัปเดทข้อมูลผู้ใช้",
    response_model=dict,
)
def patch_user(
    user_id: int,
    username: Optional[str] = Query(None, description="ชื่อผู้ใช้งาน"),
    email: Optional[EmailStr] = Query(None, description="ชื่อผู้ใช้งาน"),
):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        user_db[user_id]["username"] = username

    if email:
        user_db[user_id]["email"] = email

    return {"id": user_id, "user": user_db[user_id]}


@swagger_router.delete(
    "/{user_id}",
    summary="ลบผู้ใช้ออกจากระบบ",
    description="ลบข้อมูลผู้ใช้ตาม ID หาไม่พบ ID จะคืนค่าเป็น HTTP 404",
)
def delete_user(user_id: int):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    del user_db[user_id]
    return {"message": f"User {user_id} delete"}
