from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, auth

# Create the FastAPI app instance
app = FastAPI()

# CORS middleware to allow cross-origin requests (adjust as necessary)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to restrict specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user routes in the FastAPI app
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/", tags=["Default"])
def read_root():
    return {"message": "Welcome to the User Management API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)