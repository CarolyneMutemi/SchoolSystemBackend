from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from app.schemas.admin.auth import Admin
from app.utils.db.admin import delete_admin, edit_admin, find_all_admins
from app.utils.admin.auth import get_current_admin, register_admin


admin_management_router = APIRouter()

@admin_management_router.post("/register")
async def register_new_admin(new_admin: Admin, background_tasks: BackgroundTasks):
    """
    Register new admin.
    """
    result = register_admin(new_admin, background_tasks)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to register admin")
    return JSONResponse(content={"message": "User registered successfully"},
                        status_code=status.HTTP_201_CREATED)

@admin_management_router.get("/")
async def get_all_admins(current_admin: dict = Depends(get_current_admin)):
    """
    Get all admins.
    """
    admins = find_all_admins()
    return JSONResponse(content=admins, status_code=status.HTTP_200_OK)

@admin_management_router.put("/{admin_id}")
async def edit_an_admin(admin_id: str, new_admin: Admin, current_admin: dict = Depends(get_current_admin)):
    """
    Edit admin.
    """
    if current_admin["role"].lower() != "principal":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You do not have permission to edit an admin.")
    is_edited = edit_admin(admin_id, new_admin.model_dump())
    if not is_edited:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access.")
    return JSONResponse(content={"message": "Admin edited successfully"}, status_code=status.HTTP_200_OK)

@admin_management_router.delete("/{admin_id}")
async def delete_an_admin(admin_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete admin.
    """
    if current_admin["_id"] == admin_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete yourself.")
    if current_admin["role"].lower() != "principal":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete an admin.")
    is_deleted = delete_admin(admin_id)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access.")
    return JSONResponse(content={"message": "Admin deleted successfully"}, status_code=status.HTTP_200_OK)