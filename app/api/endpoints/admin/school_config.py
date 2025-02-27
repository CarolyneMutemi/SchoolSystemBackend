from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from app.schemas.admin.school_config import Grade, Subject, Form, Stream
from app.schemas.admin.school_config import GradeResponse, SubjectResponse, FormResponse, StreamResponse
from app.utils.db.school_config import add_grade, find_all_grades, edit_grade, delete_grade
from app.utils.db.school_config import add_subject, find_all_subjects, edit_subject, delete_subject
from app.utils.db.school_config import add_form, find_all_forms, edit_form, delete_form
from app.utils.db.school_config import add_stream, find_all_streams, edit_stream, delete_stream
from app.utils.admin.auth import get_current_admin


school_config_router = APIRouter()

@school_config_router.post("/grades", response_model=GradeResponse)
async def create_grade(grade: Grade, current_admin: dict = Depends(get_current_admin)):
    """
    Create a new grade.
    """
    new_grade = grade.model_dump()
    added_grade = add_grade(new_grade)
    return JSONResponse(content=added_grade, status_code=status.HTTP_201_CREATED)

@school_config_router.get("/grades", response_model=List[GradeResponse])
async def get_grades(current_admin: dict = Depends(get_current_admin)):
    """
    Get all grades.
    """
    grades = find_all_grades()
    return JSONResponse(content=grades, status_code=status.HTTP_200_OK)

@school_config_router.put("/grades/{grade_id}", response_model=GradeResponse)
async def edit_a_grade(grade_id: str, grade: Grade, current_admin: dict = Depends(get_current_admin)):
    """
    Edit grade.
    """
    edited_grade = edit_grade(grade_id, grade.model_dump())
    return JSONResponse(content=edited_grade, status_code=status.HTTP_200_OK)

@school_config_router.delete("/grades/{grade_id}")
async def delete_a_grade(grade_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete grade.
    """
    is_deleted = delete_grade(grade_id)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Failed to delete grade")
    return JSONResponse(content={"message": "Grade deleted successfully"}, status_code=status.HTTP_200_OK)

@school_config_router.post("/subjects")
async def create_subject(subject: Subject, current_admin: dict = Depends(get_current_admin)):
    """
    Create a new subject.
    """
    new_subject = subject.model_dump()
    added_subject = add_subject(new_subject)
    return JSONResponse(content=added_subject, status_code=status.HTTP_201_CREATED)

@school_config_router.get("/subjects", response_model=List[Subject])
async def get_subjects(current_admin: dict = Depends(get_current_admin)):
    """
    Get all subjects.
    """
    subjects = find_all_subjects()
    return JSONResponse(content=subjects, status_code=status.HTTP_200_OK)

@school_config_router.put("/subjects/{subject_id}")
async def edit_a_subject(subject_id: str, subject: Subject, current_admin: dict = Depends(get_current_admin)):
    """
    Edit subject.
    """
    edited_subject = edit_subject(subject_id, subject.model_dump())
    return JSONResponse(content=edited_subject, status_code=status.HTTP_200_OK)

@school_config_router.delete("/subjects/{subject_id}")
async def delete_a_subject(subject_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete subject.
    """
    is_deleted = delete_subject(subject_id)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Failed to delete subject")
    return JSONResponse(content={"message": "Subject deleted successfully"}, status_code=status.HTTP_200_OK)

@school_config_router.post("/forms")
async def create_form(form: Form, current_admin: dict = Depends(get_current_admin)):
    """
    Create a new form.
    """
    new_form = form.model_dump()
    added_form = add_form(new_form)
    return JSONResponse(content=added_form, status_code=status.HTTP_201_CREATED)

@school_config_router.get("/forms", response_model=List[Form])
async def get_forms(current_admin: dict = Depends(get_current_admin)):
    """
    Get all forms.
    """
    forms = find_all_forms()
    return JSONResponse(content=forms, status_code=status.HTTP_200_OK)

@school_config_router.put("/forms/{form_id}")
async def edit_a_form(form_id: str, form: Form, current_admin: dict = Depends(get_current_admin)):
    """
    Edit form.
    """
    edited_form = edit_form(form_id, form.model_dump())
    return JSONResponse(content=edited_form, status_code=status.HTTP_200_OK)

@school_config_router.delete("/forms/{form_id}")
async def delete_a_form(form_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete form.
    """
    is_deleted = delete_form(form_id)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Failed to delete form")
    return JSONResponse(content={"message": "Form deleted successfully"}, status_code=status.HTTP_200_OK)

@school_config_router.post("/streams")
async def create_stream(stream: Stream, current_admin: dict = Depends(get_current_admin)):
    """
    Create a new stream.
    """
    new_stream = stream.model_dump()
    added_stream = add_stream(new_stream)
    return JSONResponse(content=added_stream, status_code=status.HTTP_201_CREATED)

@school_config_router.get("/streams", response_model=List[Stream])
async def get_streams(current_admin: dict = Depends(get_current_admin)):
    """
    Get all streams.
    """
    streams = find_all_streams()
    return JSONResponse(content=streams, status_code=status.HTTP_200_OK)

@school_config_router.put("/streams/{stream_id}")
async def edit_a_stream(stream_id: str, stream: Stream, current_admin: dict = Depends(get_current_admin)):
    """
    Edit stream.
    """
    edited_stream = edit_stream(stream_id, stream.model_dump())
    return JSONResponse(content=edited_stream, status_code=status.HTTP_200_OK)

@school_config_router.delete("/streams/{stream_id}")
async def delete_a_stream(stream_id: str, current_admin: dict = Depends(get_current_admin)):
    """
    Delete stream.
    """
    is_deleted = delete_stream(stream_id)
    if not is_deleted:
        raise HTTPException(status_code=400, detail="Failed to delete stream")
    return JSONResponse(content={"message": "Stream deleted successfully"}, status_code=status.HTTP_200_OK)
