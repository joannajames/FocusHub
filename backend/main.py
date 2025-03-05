from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< Updated upstream
from controller import router
=======
from controller import router  # Import the controller
>>>>>>> Stashed changes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
<<<<<<< Updated upstream
    allow_origins=["*"],  # Open to intranet users
=======
    allow_origins=["*"],  # Adjust for production (e.g., ["http://localhost:5173"])
    allow_credentials=True,
>>>>>>> Stashed changes
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< Updated upstream
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "FocusHub API is running"}
=======
# ✅ Include API routes from `controller.py`
app.include_router(router)
>>>>>>> Stashed changes
