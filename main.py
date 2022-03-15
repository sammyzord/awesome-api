from fastapi import FastAPI
from src.routers import post

app = FastAPI()

app.include_router(post.router, prefix="/posts")
