from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.utils.admin.auth import register_admin
from app.schemas.admin.auth import Admin
from app.utils.shared.auth import generate_access_token, generate_refresh_token, verify_password
from app.utils.shared.auth import validate_token, delete_tokens_from_session
from app.utils.db.admin import find_admin_by_email


admin_auth_router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@admin_auth_router.post("/admin/logout")
async def logout(access_token: str = Depends(oauth2_scheme)):
    access_token_payload = validate_token(access_token, "access")
    session_id = access_token_payload.get("session_id")
    # Delete the tokens from the database
    are_deleted = delete_tokens_from_session(session_id)

    if not are_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not log out.")
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Logged out successfully."})
