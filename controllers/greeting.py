from fastapi import APIRouter

greeting_router = APIRouter(
    prefix="/greeting",
    tags=["wellcome"]
)

@greeting_router.get("/hello")
async def hello():
    return {"message": "Hello World"}


@greeting_router.get("/hi/{fname}")
async def hi(fname):
    return {"message": f"Hi: {fname}"}


@greeting_router.delete("/remove")
async def remove_data():
    return {"message": "removedata"}