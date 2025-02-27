from fastapi import Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer


from app.utils.shared.auth import validate_token
from app.utils.db.students import get_student_by_admission_number

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_student(access_token: str = Depends(oauth2_scheme)):
    """
    Get current student.
    """
    access_token_payload = validate_token(access_token, "access")
    admission_number = access_token_payload.get("sub")
    print("student's admission_number is: ", admission_number)
    student = get_student_by_admission_number(admission_number)
    print("student: ", student)
    if not student:
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    student["_id"] = str(student["_id"])
    return student