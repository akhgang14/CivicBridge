from dotenv import load_dotenv
load_dotenv()

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router
from api import document


app = FastAPI(title="CivicBridge API")

frontend_url=os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router, prefix="/api")
app.include_router(document.router,prefix="/api")


@app.get("/")
def root():
    return {
        "message": "CivicBridge API is running 🚀"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "civicbridge-api"
    }