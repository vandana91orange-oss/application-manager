from fastapi import HTTPException
from app.utils.password import generate_temporary_password
from app.core.security import hash_password
from app.tasks.email_task import send_welcome_email

class UserService:


    def __init__(
        self,
        repository
    ):

        self.repository=repository

    def create(self, user):

        exists = self.repository.get_by_email(user.email)

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        temporary_password = generate_temporary_password()

        hashed_password = hash_password(
            temporary_password
        )

        created_user = self.repository.create(
            user,
            hashed_password,
        )
        send_welcome_email.apply_async(
                kwargs={
                    "email": created_user.email,
                    "first_name": created_user.first_name,
                    "temporary_password": temporary_password,
                }
            )

        return created_user

    def get_all(self):

        return (
            self.repository
            .get_all()
        )



    def get_one(
        self,
        user_id
    ):

        user=(
            self.repository
            .get_by_id(user_id)
        )


        if not user:

            raise HTTPException(
                404,
                "User not found"
            )


        return user



    def update(
        self,
        user_id,
        data
    ):

        return (
            self.repository
            .update(
                user_id,
                data
            )
        )



    def delete(
        self,
        user_id
    ):

        return (
            self.repository
            .delete(user_id)
        )
