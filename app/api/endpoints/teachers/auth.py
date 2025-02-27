from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from uuid import uuid4

from app.utils.shared.auth import generate_access_token, generate_refresh_token, verify_password
from app.utils.shared.auth import validate_token, delete_tokens_from_session
from app.utils.db.teacher import find_teacher_by_email

teacher_auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# @teacher_auth_router.post("/teacher/login")
# async def login(login_data: OAuth2PasswordRequestForm = Depends()):
#     email = login_data.username
#     password = login_data.password

#     print(login_data)

#     teacher = find_teacher_by_email(email)
#     if not teacher:
#         print("Teacher not found")
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
    
#     print("Teacher: ", teacher)
#     if not verify_password(password, teacher.get("password")):
#         print("Password incorrect")
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
    
#     session_id = str(uuid4())
#     payload = {
#         "session_id": session_id,
#         "sub": email,
#         "role": "teacher"
#     }
#     access_token = generate_access_token(payload)
#     refresh_token = generate_refresh_token(payload)
#     print("Access token is: ", access_token)
#     print("Refresh token is: ", refresh_token)
#     return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token},
#                         status_code=status.HTTP_200_OK)

@teacher_auth_router.post("/teacher/logout")
async def logout(access_token: str = Depends(oauth2_scheme)):
    access_token_payload = validate_token(access_token, "access")
    session_id = access_token_payload.get("session_id")
    # Delete the tokens from the database
    are_deleted = delete_tokens_from_session(session_id)

    if not are_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not log out.")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out successfully."})

