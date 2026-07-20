from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.models.users import User
from app.repositories.role_repository import RoleRepository

class UserRepository:


    def __init__(
        self,
        db:Session
    ):
        self.db=db



    def create(
        self,
        user,
        hashed_password
    ):

        obj=User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
            role_id=user.role_id
        )


        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj



    def get_all(self):

        return (
            self.db.query(User)
            .options(
                joinedload(User.role)
            )
            .all()
        )



    def get_by_id(
        self,
        user_id:int
    ):

        return (
            self.db.query(User)
            .options(
                joinedload(User.role)
            )
            .filter(
                User.id==user_id
            )
            .first()
        )



    def get_by_email(self, email: str):
        if not email:
            return None

        return (
            self.db.query(User)
            .filter(User.email.ilike(email.strip()))
            .first()
        )

    def update(
        self,
        user_id,
        data
    ):

        user=self.get_by_id(user_id)

        if not user:
            return None

        role = data.role_id

        role_repo = RoleRepository(self.db)
        role = (
                role_repo.get_by_id(data.role_id)
            )
        
        if not role:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid role id"
                )

        for key,value in data.dict(
            exclude_unset=True
        ).items():

            setattr(
                user,
                key,
                value
            )
        
        self.db.commit()
        self.db.refresh(user)

        return user


    def delete(
        self,
        user_id
    ):

        user=self.get_by_id(user_id)

        if user:

            self.db.delete(user)
            self.db.commit()

        return user
    
    def delete_user_tokens(self, user_id: int):

        self.db.query(
            PasswordResetToken
        ).filter(
            PasswordResetToken.user_id == user_id
        ).delete()

        self.db.commit()

    def token_create(
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

    def token_delete(self, reset: PasswordResetToken):

        self.db.delete(reset)

        self.db.commit()
    

    def update_password(self, user: User, hashed_password: str):
        user.hashed_password = hashed_password
        self.db.commit()
        self.db.refresh(user)
        return user
