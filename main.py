from fastapi import FastAPI

app = FastAPI()

from Routes.auth_routes import auth_router
from Routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# Use para rodar o codigo uvicorn main:app --reload