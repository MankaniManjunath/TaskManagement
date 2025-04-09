
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

# Import the get_db function to manage database connections
from models.connection import get_db


# Import user-related models and functions from the authController
from controller.authController import (
    UserCreate, UserResponse, Token, authenticate_user, 
    create_access_token, get_current_active_user, create_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Create an instance of APIRouter with a prefix for user-related routes
router = APIRouter(prefix="/api/users", tags=["users"])

# user registration, which accepts a UserCreate model and returns a UserResponse
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Call the create_user function to add a new user to the database
    return create_user(db=db, user=user)

#route for user login that returns a token for authentication
@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Authenticate the user using the provided username and password
    user = authenticate_user(db, form_data.username, form_data.password)
    # If authentication fails, raise an HTTP exception with a 401 status code
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Set the expiration time for the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create a new access token for the authenticated user
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # Return the access token and its type
    return {"access_token": access_token, "token_type": "bearer"}

# route to get the current user's information
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user = Depends(get_current_active_user)):
    # Return the current user's details
    return current_user