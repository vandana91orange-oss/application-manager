from datetime import datetime

from sqlalchemy.orm import Session

from app.models.password_reset import PasswordResetToken


class PasswordResetRepository:

    def __init__(self, db: Session):
        self.db = db

    def delete_user_tokens(self, user_id: int):

        self.db.query(
            PasswordResetToken
        ).filter(
            PasswordResetToken.user_id == user_id
        ).delete()

        self.db.commit()

    def create(
        self,
        user_id: int,
        token: str,
        expires_at: datetime,
    ):

        reset = PasswordResetToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )

        self.db.add(reset)

        self.db.commit()

        self.db.refresh(reset)

        return reset

    def get_by_token(self, token: str):

        return (
            self.db.query(
                PasswordResetToken
            )
            .filter(
                PasswordResetToken.token == token
            )
            .first()
        )

    def delete(self, reset: PasswordResetToken):

        self.db.delete(reset)

        self.db.commit()