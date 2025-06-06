from fastapi import APIRouter
import jwt

auth_router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@auth_router.get("/token")
async def token():
    with open("private_key.pem", "rb") as f:
        private_key = f.read()

    user_info = {
        "id":1234,
        "name":"Somchai Jaidee",
        "email":"somchai@example.com",
        "role":"admin"
    }

    token = jwt.encode(
        user_info,
        private_key,
        algorithm="RS256"
    )

    return {
        "token": token
    }