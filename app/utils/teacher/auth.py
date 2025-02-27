from fastapi import Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer


from app.utils.shared.auth import validate_token
from app.utils.db.teacher import find_teacher_by_email
from app.utils.shared.auth import generate_random_password, hash_password, send_password_to_email
from app.utils.db.teacher import insert_new_teacher
from app.utils.teacher.class_management import class_exists, all_subject_codes
from app.utils.db.user import user_added_to_index
from app.schemas.teacher.auth import Teacher

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def register_teacher(new_teacher: Teacher, background_tasks: BackgroundTasks):
    """
    Register new teacher.
    """
    for class_in_charge in new_teacher.classes_in_charge:
        print("Class in charge: ", class_in_charge)
        class_exists(class_in_charge.form, class_in_charge.stream)

    for class_taught in new_teacher.classes_taught:
        print("Class taught: ", class_taught)
        class_exists(class_taught.form, class_taught.stream)
        if class_taught.subject not in all_subject_codes():
            raise HTTPException(status_code=400, detail="Subject does not exist.")
        
    new_teacher = new_teacher.model_dump()
    email = new_teacher["email"]
    teacher = find_teacher_by_email(email)
    if teacher:
        raise HTTPException(status_code=400, detail="Teacher already exists.")
    is_added_to_index = user_added_to_index(email, "teacher")
    if not is_added_to_index:
        raise HTTPException(status_code=400, detail="Could not add user to index.")
    generated_password = generate_random_password()
    new_teacher["password"] = hash_password(generated_password)
    is_added = insert_new_teacher(new_teacher)
    if is_added:
        background_tasks.add_task(send_password_to_email, new_teacher["email"], generated_password)
        del new_teacher["password"]
        return new_teacher
    else:
        return None

def get_current_teacher(access_token: str = Depends(oauth2_scheme)):
    """
    Get current teacher.
    """
    access_token_payload = validate_token(access_token, "access")
    email = access_token_payload.get("sub")
    print("Teacher's email is: ", email)
    teacher = find_teacher_by_email(email)
    print("Teacher: ", teacher)
    if not teacher:
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    teacher["_id"] = str(teacher["_id"])
    return teacher