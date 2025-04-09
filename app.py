from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from models.connection import engine, Base
from router.userRoutes import router as user_router
from router.tasksRoutes import router as task_router

load_dotenv()

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Task Management API"}