from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas.student.result import SubjectResult
from app.utils.teacher.auth import get_current_teacher
from app.utils.teacher.result_management import add_or_update_subject_result, get_all_results_for_subject


results_router = APIRouter()

@results_router.post("/")
async def add_or_update_subject_results(result: SubjectResult, current_teacher: dict = Depends(get_current_teacher)):
    """
    Add or update a subject result.
    """
    response = add_or_update_subject_result(result, current_teacher)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)

@results_router.get("/")
async def get_all_year_results_for_subject(subject: str, year: int, form: int, stream: str, current_teacher: dict = Depends(get_current_teacher)):
    """
    Get all student results for a subject in a year.
    """
    result = get_all_results_for_subject(subject, year, form, stream, current_teacher)
    return JSONResponse(content=result, status_code=status.HTTP_200_OK)
