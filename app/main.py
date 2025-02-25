from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.admin.auth import admin_auth_router
from app.api.endpoints.auth import auth_router


app = FastAPI()

app.include_router(admin_auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
