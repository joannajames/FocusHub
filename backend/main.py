from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open to intranet users
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "FocusHub API is running"}
