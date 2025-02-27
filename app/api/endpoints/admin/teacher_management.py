"""
Teacher management endpoints.
"""
from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from app.schemas.teacher.auth import Teacher
from app.utils.admin.auth import get_current_admin
from app.utils.teacher.auth import register_teacher
from app.utils.db.teacher import find_all_teachers, edit_teacher, delete_teacher


admin_teacher_router = APIRouter()

@admin_teacher_router.post("/", )
async def create_teacher(teacher: Teacher, background_tasks: BackgroundTasks, current_admin: dict = Depends(get_current_admin)):
    """
    Create a new teacher.
    """
    added_teacher = register_teacher(teacher, background_tasks)
    return JSONResponse(content=added_teacher, status_code=status.HTTP_201_CREATED)

@admin_teacher_router.get("/")
async def get_teachers(current_admin: dict = Depends(get_current_admin)):
    """
    Get all teachers.
    """
    teachers = find_all_teachers()
    return JSONResponse(content=teachers, status_code=status.HTTP_200_OK)

@admin_teacher_router.put("/{teacher_id}")
async def edit_a_teacher(teacher_id: str, teacher: Teacher, current_admin: dict = Depends(get_current_admin)):
    """
    Edit teacher.
    """
    edited_teacher = edit_teacher(teacher_id, teacher.model_dump())
    return JSONResponse(content=edited_teacher, status_code=status.HTTP_200_OK)

@admin_teacher_router.delete("/{teacher_id}")
async def delete_a_teacher(teacher_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete teacher.
    """
    is_deleted = delete_teacher(teacher_id)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Failed to delete teacher")
    return JSONResponse(content={"message": "Teacher deleted successfully"}, status_code=status.HTTP_200_OK)
