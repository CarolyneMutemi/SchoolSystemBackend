from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


from app.utils.teacher.auth import get_current_teacher
from app.utils.db.students import get_students_in_a_class
from app.utils.teacher.class_management import register_student, edit_a_student, delete_a_student
from app.schemas.student.profile import Student
from app.schemas.teacher.auth import Class
from app.utils.teacher.class_management import is_the_class_teacher

class_router = APIRouter()



@class_router.get("/students", response_model=list[Student])
async def get_class_students(form: int, stream: str, current_teacher: dict = Depends(get_current_teacher)):
    """
    Get all students in the class a teacher is in charge of.
    """
    class_obj = Class(form=form, stream=stream)
    # Check if the teacher is in charge of the class
    is_the_class_teacher(class_obj, current_teacher)
    
    students = get_students_in_a_class(form, stream)
    return JSONResponse(content=students, status_code=status.HTTP_200_OK)

@class_router.post("/students", response_model=Student)
async def add_student_to_class(student: Student, current_teacher: dict = Depends(get_current_teacher)):
    """
    Add a student to a class.
    """
    student.stream = student.stream.lower()
    added_student = register_student(student, current_teacher)
    return JSONResponse(content=added_student, status_code=status.HTTP_201_CREATED)

@class_router.put("/students/{student_id}", response_model=Student)
async def edit_student_in_class(student_id: str, student: Student, current_teacher: dict = Depends(get_current_teacher)):
    """
    Edit a student in a class.
    """
    edited_student = edit_a_student(student_id, student)
    return JSONResponse(content=edited_student, status_code=status.HTTP_200_OK)

@class_router.delete("/students/{student_id}")
async def delete_student_in_class(student_id: str, current_teacher: dict = Depends(get_current_teacher)):
    """
    Delete a student in a class.
    """
    delete_a_student(student_id, current_teacher)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Student deleted successfully."})