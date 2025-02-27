from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.utils.admin.auth import hash_password
from app.utils.teacher.auth import get_current_teacher
from app.utils.db.teacher import edit_teacher
from app.schemas.admin.auth import NewPassword

teacher_profile_router = APIRouter()

@teacher_profile_router.get("/me")
async def get_profile(current_teacher: dict = Depends(get_current_teacher)):
    """
    Get current teacher profile.
    """
    return JSONResponse(content=current_teacher, status_code=status.HTTP_200_OK)

@teacher_profile_router.put("/me")
async def change_password(password: NewPassword, current_teacher: dict = Depends(get_current_teacher)):
    """
    Change teacher password.
    """
    current_teacher_id = current_teacher["_id"]
    new_password = password.password
    hashed_password = hash_password(new_password)

    edit_teacher(current_teacher_id, {"password": hashed_password})
    return JSONResponse(content={"message": "Password changed successfully"}, status_code=status.HTTP_200_OK)
