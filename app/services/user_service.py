import math
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
        send_welcome_email.delay(
                to_email=user.email,
                subject="Welcome !!",
                first_name=user.first_name,
                temporary_password=temporary_password,
            )
        return created_user

    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
        role_id: int | None = None,
        is_active: bool | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ):
        users, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            search=search,
            role_id=role_id,
            is_active=is_active,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        return {
            "items": users,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size) if total else 0,
        }



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
