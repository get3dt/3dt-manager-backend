from fastapi import FastAPI

from app.api.v1.user_routes import router as user_routes

app = FastAPI()

app.include_router(user_routes)
