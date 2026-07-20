from fastapi import HTTPException
from datetime import datetime,timedelta

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token
)

from datetime import datetime, timedelta
import secrets

from sqlalchemy.orm import Session
from app.repositories.password_repository import PasswordResetRepository
from app.repositories.user_repository import UserRepository

from app.models.password_reset import PasswordResetToken
from app.models.users import User

from app.core.security import hash_password

from app.utils.send_password_email import send_reset_email

class AuthService:


    def __init__(
        self,
        user_repo,
        token_repo,
    ):

        self.user_repo=user_repo
        self.token_repo=token_repo



    def login(
        self,
        email,
        password
    ):

        user=(
            self.user_repo
            .get_user_by_email(email)
        )


        if not user:
            raise HTTPException(
                401,
                "Invalid login"
            )


        if not verify_password(
            password,
            user.hashed_password
        ):

            raise HTTPException(
                401,
                "Invalid login"
            )


        payload={
            "sub":str(user.id),
            "role":user.role.name
        }


        access=create_access_token(
            payload
        )


        refresh=create_refresh_token(
            payload
        )


        self.token_repo.create(
            user.id,
            refresh,
            datetime.utcnow()
            +
            timedelta(days=7)
        )


        return {
            "access_token":access,
            "refresh_token":refresh,
            "token_type":"bearer"
        }



    def logout(
        self,
        refresh_token
    ):

        self.token_repo.revoke(
            refresh_token
        )


        return {
            "message":
            "Logout successful"
        }


class ForgetPasswordService:

    def __init__(self, db):
        self.user_repo = UserRepository(db)
        self.reset_repo = PasswordResetRepository(db)

    def forgot_password(self, email: str):

        user = self.user_repo.get_by_email(email)

        if user:

            self.reset_repo.delete_user_tokens(user.id)

            token = secrets.token_urlsafe(32)

            self.reset_repo.create(
                user_id=user.id,
                token=token,
                expires_at=datetime.utcnow()
                + timedelta(minutes=15),
            )

            send_reset_email(
                user.email,
                token,
            )

        return {
            "message": "If an account exists, a password reset email has been sent."
        }

    def reset_password(
        self,
        token: str,
        new_password: str,
    ):

        reset = self.reset_repo.get_by_token(token)

        if not reset:
            return False

        if reset.expires_at < datetime.utcnow():

            self.reset_repo.delete(reset)

            return False

        user = self.user_repo.get_by_id(reset.user_id)

        self.user_repo.update_password(
            user,
            hash_password(new_password),
        )

        self.reset_repo.delete(reset)

        return True
