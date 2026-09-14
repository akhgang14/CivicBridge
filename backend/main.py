from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CivicBridge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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