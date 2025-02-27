from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from app.utils.shared.auth import hash_password, verify_password
from app.utils.admin.auth import get_current_admin
from app.utils.db.admin import edit_admin
from app.schemas.admin.auth import NewPassword

profile_router = APIRouter()

@profile_router.get("/me")
async def get_profile(current_admin: dict = Depends(get_current_admin)):
    """
    Get current admin profile.
    """
    del current_admin["password"]
    return JSONResponse(content=current_admin, status_code=status.HTTP_200_OK)

@profile_router.put("/me")
async def change_password(password: NewPassword, current_admin: dict = Depends(get_current_admin)):
    """
    Change admin password.
    """
    old_password = password.current_password
    if not verify_password(old_password, current_admin["password"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    current_admin_id = current_admin["_id"]
    new_password = password.new_password
    hashed_password = hash_password(new_password)

    edit_admin(current_admin_id, {"password": hashed_password})
    return JSONResponse(content={"message": "Password changed successfully"}, status_code=status.HTTP_200_OK)
