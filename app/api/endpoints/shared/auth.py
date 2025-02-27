from fastapi import APIRouter, Depends, HTTPException, Header, status, BackgroundTasks, Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from uuid import uuid4
from uuid import uuid4

from app.utils.shared.auth import generate_access_token, generate_refresh_token
from app.utils.shared.auth import validate_token, verify_password
from app.utils.db.user import get_user_by_identifier
from app.utils.student.auth import get_student_by_admission_number
from app.utils.admin.auth import find_admin_by_email
from app.utils.teacher.auth import find_teacher_by_email


auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user.
    """
    identifier = form_data.username
    password = form_data.password

    print(form_data)

    user = get_user_by_identifier(identifier)
    if not user:
        print("user not found")
        raise HTTPException(status_code=401, detail="Incorrect identifier or password")
    
    role = user.get("role")
    find_user = {
        "student": get_student_by_admission_number,
        "admin": find_admin_by_email,
        "teacher": find_teacher_by_email
    }

    user_obj = find_user.get(role)(identifier)
    if not user_obj:
        print("User not found")
        raise HTTPException(status_code=401, detail="Incorrect identifier or password")
    print("user: ", user_obj)
    if not verify_password(password, user_obj.get("password")):
        print("Password incorrect")
        raise HTTPException(status_code=401, detail="Incorrect identifier or password")
    
    session_id = str(uuid4())
    payload = {
        "session_id": session_id,
        "sub": identifier,
        "role": role
    }
    access_token = generate_access_token(payload)
    refresh_token = generate_refresh_token(payload)
    print("Access token is: ", access_token)
    print("Refresh token is: ", refresh_token)
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token},
                        status_code=status.HTTP_200_OK)

@auth_router.post("/refresh")
async def refresh(authorization: str = Header(...)):
    # Ensure the token is in the format "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    refresh_token = authorization.split("Bearer ")[1]  # Extract the token

    # Validate the refresh token
    refresh_token_payload = validate_token(refresh_token, "refresh")

    # Generate a new access token
    access_token = generate_access_token(refresh_token_payload)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "token_type": "bearer"})
