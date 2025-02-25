from app.db.mongo_db import admins_collection


def find_admin_by_email(email: str):
    """
    Find admin by email.
    """
    print("Finding admin by email")
    admin = admins_collection.find_one({"email": email})
    return admin
