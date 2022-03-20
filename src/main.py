from fastapi import FastAPI
from .routers import post, auth

app = FastAPI()

app.include_router(post.router, prefix="/posts")
app.include_router(auth.router, prefix="/auth")
