from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.utils.admin.auth import hash_password
from app.utils.admin.auth import get_current_admin
from app.utils.db.admin import edit_admin
from app.schemas.admin.auth import NewPassword

profile_router = APIRouter()

@profile_router.get("/me")
async def get_profile(current_admin: dict = Depends(get_current_admin)):
    """
    Get current admin profile.
    """
    return JSONResponse(content=current_admin, status_code=status.HTTP_200_OK)

@profile_router.put("/me")
async def change_password(password: NewPassword, current_admin: dict = Depends(get_current_admin)):
    """
    Change admin password.
    """
    current_admin_id = current_admin["_id"]
    new_password = password.password
    hashed_password = hash_password(new_password)

    edit_admin(current_admin_id, {"password": hashed_password})
    return JSONResponse(content={"message": "Password changed successfully"}, status_code=status.HTTP_200_OK)
