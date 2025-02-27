from fastapi import BackgroundTasks, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.schemas.admin.auth import Admin
from app.utils.shared.auth import generate_random_password, hash_password, send_password_to_email, validate_token
from app.utils.db.admin import find_admin_by_email, insert_new_admin
from app.utils.db.user import user_added_to_index


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def register_admin(new_admin: Admin, background_tasks: BackgroundTasks):
    """
    Register new admin.
    """
    new_admin = new_admin.model_dump()
    email = new_admin["email"]
    admin = find_admin_by_email(email)
    if admin:
        raise HTTPException(status_code=400, detail="Admin already exists.")
    is_added_to_index = user_added_to_index(email, "admin")
    if not is_added_to_index:
        raise HTTPException(status_code=400, detail="Could not add user to index.")
    generated_password = generate_random_password()
    new_admin["password"] = hash_password(generated_password)
    is_added = insert_new_admin(new_admin)
    if is_added:
        background_tasks.add_task(send_password_to_email, new_admin["email"], generated_password)
        del new_admin["password"]
        return new_admin
    else:
        return None

def get_current_admin(access_token: str = Depends(oauth2_scheme)):
    """
    Get current admin.
    """
    access_token_payload = validate_token(access_token, "access")
    email = access_token_payload.get("sub")
    admin = find_admin_by_email(email)
    if not admin:
        raise HTTPException(status_code=401, detail="Unauthorized access.")
    print("Admin: ", admin)
    return admin
