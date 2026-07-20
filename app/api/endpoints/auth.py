from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db

from app.services.auth_service import AuthService, ForgetPasswordService
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest, 
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.repositories.auth_repository import AuthRepository, TokenRepository


router=APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


def get_auth_service(
    db: Session = Depends(get_db)
):

    user_repository = AuthRepository(db)

    token_repository = TokenRepository(db)

    return AuthService(
        user_repository,
        token_repository,
    )


@router.post("/login")
def login(
    data: LoginRequest,
    service: AuthService =Depends(get_auth_service)
):

    return service.login(
        data.email,
        data.password
    )



@router.post("/logout")
def logout(
    data:RefreshTokenRequest,
    service=Depends(get_auth_service)
):

    return service.logout(
        data.refresh_token
    )

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):

    service = ForgetPasswordService(db)

    return service.forgot_password(request.email)


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):

    service = ForgetPasswordService(db)

    success = service.reset_password(
        request.token,
        request.new_password,
    )

    if not success:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired token.",
        )

    return {
        "message": "Password reset successful."
    }
