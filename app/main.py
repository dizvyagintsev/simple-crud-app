from fastapi import FastAPI

from app.routers import user_profile

app = FastAPI()

app.include_router(user_profile.router)
