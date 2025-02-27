from fastapi import HTTPException

from app.utils.db.results import add_or_update_subject_results, get_all_subject_results
from app.schemas.student.result import SubjectResult
from app.utils.db.school_config import find_all_grades


def teaches_subject_in_class(form: int, stream: str, subject: str, teacher: dict) -> bool:
    """
    Check if a teacher teaches a subject in a class.
    """
    classes_taught = teacher.get("classes_taught")
    for class_taught in classes_taught:
        class_form = class_taught.get("form")
        class_stream = class_taught.get("stream")
        class_subject = class_taught.get("subject")
        if class_form == form and class_stream == stream and class_subject == subject:
            return True
    return False

def calculate_grade(marks: int) -> str:
    """
    Calculate the grade of a student.
    """
    all_grades = find_all_grades()
    for grade in all_grades:
        if marks >= grade.get("min_score") and marks <= grade.get("max_score"):
            return grade.get("letter")
    return "F"

def add_or_update_subject_result(result: SubjectResult, teacher: dict) -> dict:
    """
    Add or update a subject result.
    """
    if not teaches_subject_in_class(result.form, result.stream, result.subject, teacher):
        raise HTTPException(status_code=400, detail="Teacher does not teach the subject in the class.")
    result_dict = result.model_dump()
    result_dict["grade"] = calculate_grade(result_dict["marks"])
    response = add_or_update_subject_results(result_dict)
    return response

def get_all_results_for_subject(subject: str, year: int, form: int, stream: str, teacher: dict) -> list:
    """
    Get all student results for a subject in a year.
    """
    if not teaches_subject_in_class(form, stream, subject, teacher):
        raise HTTPException(status_code=400, detail="Teacher does not teach the subject in the class.")
    results = get_all_subject_results(subject, year, form, stream)
    return results
