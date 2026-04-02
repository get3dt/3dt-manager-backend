from fastapi import FastAPI

from app.api.v1 import user_router

app = FastAPI()

app.include_router(user_router)
