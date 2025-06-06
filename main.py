from fastapi import FastAPI
from controllers.greeting import greeting_router
from controllers.organization import org_router
from controllers.user import user_router
from controllers.product import product_router
from controllers.auth import auth_router
from controllers.swagger import swagger_router

app = FastAPI()

app.include_router(greeting_router)
app.include_router(org_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(auth_router)
app.include_router(swagger_router)
