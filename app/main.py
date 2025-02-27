from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.db.counter import initialize_counter
from app.api.endpoints.admin.auth import admin_auth_router
from app.api.endpoints.shared.auth import auth_router
from app.api.endpoints.admin.school_config import school_config_router
from app.api.endpoints.admin.teacher_management import admin_teacher_router
from app.api.endpoints.admin.admin_management import admin_management_router
from app.api.endpoints.admin.profile import profile_router
from app.api.endpoints.teachers.auth import teacher_auth_router
from app.api.endpoints.teachers.class_management import class_router
from app.api.endpoints.teachers.results_management import results_router
from app.api.endpoints.teachers.profile import teacher_profile_router
from app.api.endpoints.students.auth import student_auth_router
from app.api.endpoints.students.profile import student_profile_router
from app.db.mongo_db import students_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs setup tasks when FastAPI starts."""
    initialize_counter()  # Ensure the counter is initialized
    yield  # Continue running the app

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

app.include_router(admin_auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(school_config_router, prefix="/config", tags=["School System Configuration"])
app.include_router(profile_router, prefix="/admins", tags=["Profile"])
app.include_router(admin_management_router, prefix="/admins", tags=["Admin Management"])
app.include_router(teacher_profile_router, prefix="/teachers", tags=["Profile"])
app.include_router(admin_teacher_router, prefix="/teachers", tags=["Teacher Management"])
app.include_router(teacher_auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(class_router, prefix="/class", tags=["Class Management"])
app.include_router(results_router, prefix="/results", tags=["Results Management"])
app.include_router(student_auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(student_profile_router, prefix="/students", tags=["Profile"])

print(students_collection.find_one({"admission_number": 1001}))

