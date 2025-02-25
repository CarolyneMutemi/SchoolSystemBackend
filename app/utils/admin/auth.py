from fastapi import BackgroundTasks

from app.schemas.admin.auth import NewAdmin
from app.db.mongo_db import admins_collection
from app.utils.shared.auth import generate_random_password, hash_password, send_password_to_email


def register_admin(new_admin: NewAdmin, background_tasks: BackgroundTasks):
    """
    Register new admin.
    """
    new_admin = new_admin.model_dump()
    generated_password = generate_random_password()
    new_admin["password"] = hash_password(generated_password)
    result = admins_collection.insert_one(new_admin)
    if result.acknowledged:
        background_tasks.add_task(send_password_to_email, new_admin["email"], generated_password)
        del new_admin["password"]
        return new_admin
    else:
        return None
