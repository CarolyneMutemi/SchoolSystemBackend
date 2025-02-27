from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.responses import JSONResponse
from app.utils.shared.auth import generate_access_token
from app.utils.shared.auth import validate_token


auth_router = APIRouter(tags=["Authentication"])

@auth_router.post("/refresh")
async def refresh(authorization: str = Header(...)):
    # Ensure the token is in the format "Bearer <token>"
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    refresh_token = authorization.split("Bearer ")[1]  # Extract the token

    # Validate the refresh token
    refresh_token_payload = validate_token(refresh_token, "refresh")

    # Generate a new access token
    access_token = generate_access_token(refresh_token_payload)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": access_token, "token_type": "bearer"})
