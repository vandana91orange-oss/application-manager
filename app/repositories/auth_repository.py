from sqlalchemy.orm import Session
from app.models.users import User
from app.models.refresh_token import RefreshToken


class AuthRepository:


    def __init__(
        self,
        db: Session
    ):
        self.db = db



    def get_user_by_email(
        self,
        email: str
    ):

        return (
            self.db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )



class TokenRepository:


    def __init__(
        self,
        db:Session
    ):

        self.db=db



    def create(
        self,
        user_id,
        token,
        expires
    ):

        obj=RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires
        )

        self.db.add(obj)
        self.db.commit()

        return obj



    def get(
        self,
        token
    ):

        return (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.token==token,
                RefreshToken.is_revoked==False
            )
            .first()
        )



    def revoke(
        self,
        token
    ):

        obj=self.get(token)

        if obj:
            obj.is_revoked=True
            self.db.commit()

        return obj