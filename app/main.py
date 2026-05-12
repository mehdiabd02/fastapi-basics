from app.routers import votes
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

try:
    models.Base.metadata.create_all(bind=engine)
except Exception:
    # In CI or when the database isn't ready at import time, skip creating tables here.
    # Tests create/drop tables in fixtures and production should use migrations.
    pass


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)



@app.get("/")
def root():
    return {"message": "Hello World!!!"}



