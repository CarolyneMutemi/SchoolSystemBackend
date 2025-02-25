from fastapi import APIRouter, Depends, HTTPException, Header, status, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from uuid import uuid4
from typing import Annotated
from pydantic import BaseModel
from uuid import uuid4

from app.utils.admin.auth import register_admin
from app.schemas.admin.auth import NewAdmin
from app.utils.shared.auth import generate_access_token, generate_refresh_token, verify_password
from app.utils.shared.auth import validate_token, delete_tokens_from_session
from app.utils.admin.db import find_admin_by_email


admin_auth_router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/admin/login")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@admin_auth_router.post("/admin/register")
async def register_new_admin(new_admin: NewAdmin, background_tasks: BackgroundTasks):
    """
    Register new admin.
    """
    result = register_admin(new_admin, background_tasks)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to register admin")
    return JSONResponse(content={"message": "User registered successfully"},
                        status_code=status.HTTP_201_CREATED)

@admin_auth_router.post("/admin/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login admin.
    """
    email = form_data.username
    password = form_data.password

    print(form_data)

    admin = find_admin_by_email(email)
    if not admin:
        print("Admin not found")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    if not verify_password(password, admin.get("password")):
        print("Password incorrect")
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    session_id = str(uuid4())
    payload = {
        "session_id": session_id,
        "sub": email,
        "token_type": "access",
        "role": "admin"
    }
    access_token = generate_access_token(payload)
    refresh_token = generate_refresh_token(payload)
    print("Access token is: ", access_token)
    print("Refresh token is: ", refresh_token)
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token},
                        status_code=status.HTTP_200_OK)

@admin_auth_router.post("/admin/logout")
async def logout(access_token: str = Depends(oauth2_scheme)):
    access_token_payload = validate_token(access_token, "access")
    session_id = access_token_payload.get("session_id")
    # Delete the tokens from the database
    are_deleted = delete_tokens_from_session(session_id)

    if not are_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not log out.")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out successfully."})

