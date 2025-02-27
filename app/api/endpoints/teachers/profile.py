from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from app.utils.shared.auth import hash_password, verify_password
from app.utils.teacher.auth import get_current_teacher
from app.utils.db.teacher import edit_teacher
from app.schemas.admin.auth import NewPassword

teacher_profile_router = APIRouter()

@teacher_profile_router.get("/me")
async def get_profile(current_teacher: dict = Depends(get_current_teacher)):
    """
    Get current teacher profile.
    """
    del current_teacher["password"]
    return JSONResponse(content=current_teacher, status_code=status.HTTP_200_OK)

@teacher_profile_router.put("/me")
async def change_password(password: NewPassword, current_teacher: dict = Depends(get_current_teacher)):
    """
    Change teacher password.
    """
    old_password = password.current_password
    if not verify_password(old_password, current_teacher["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    current_teacher_id = current_teacher["_id"]
    new_password = password.new_password
    hashed_password = hash_password(new_password)

    edit_teacher(current_teacher_id, {"password": hashed_password})
    return JSONResponse(content={"message": "Password changed successfully"}, status_code=status.HTTP_200_OK)
