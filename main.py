from fastapi import FastAPI
from fastapi.security import OAuth2AuthorizationCodeBearer

from api import users

app = FastAPI()
app.include_router(users.router)
