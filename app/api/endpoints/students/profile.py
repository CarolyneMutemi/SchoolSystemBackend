from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from app.utils.shared.auth import hash_password, verify_password
from app.utils.student.auth import get_current_student
from app.utils.db.students import edit_student
from app.schemas.admin.auth import NewPassword

student_profile_router = APIRouter()

@student_profile_router.get("/me")
async def get_profile(current_student: dict = Depends(get_current_student)):
    """
    Get current student profile.
    """
    del current_student["password"]
    return JSONResponse(content=current_student, status_code=status.HTTP_200_OK)

@student_profile_router.put("/me")
async def change_password(password: NewPassword, current_student: dict = Depends(get_current_student)):
    """
    Change student password.
    """
    old_password = password.current_password
    if not verify_password(old_password, current_student["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    current_student_id = current_student["_id"]
    new_password = password.new_password
    hashed_password = hash_password(new_password)

    edit_student(current_student_id, {"password": hashed_password})
    return JSONResponse(content={"message": "Password changed successfully"}, status_code=status.HTTP_200_OK)
