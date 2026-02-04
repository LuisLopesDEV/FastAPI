from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCES_TOKEN_EXPIRES_MINUTES = os.getenv('ACCES_TOKEN_EXPIRES_MINUTES')
app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from Routes.auth_routes import auth_router
from Routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# Use para rodar o codigo uvicorn main:app --reload