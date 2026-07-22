from datetime import datetime
from sqlalchemy import func, or_, select
from sqlalchemy.orm import selectinload, Session, joinedload
from app.models.password_reset import PasswordResetToken
from fastapi import HTTPException

from app.models.users import User
from app.repositories.role_repository import RoleRepository

class UserRepository:


    def __init__(
        self,
        db:Session
    ):
        self.db=db

    SORTABLE_COLUMNS = {
        "id": User.id,
        "first_name": User.first_name,
        "last_name": User.last_name,
        "email": User.email,
        "created_at": User.created_at,
        
    }

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



    def get_all(
        self,
        page: int = 1,
        page_size: int = 10,
        search: str | None = None,
        role_id: int | None = None,
        is_active: bool | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[User], int]:

        filters = []

        # Search by first name, last name or email
        if search:
            normalized_search = search.strip()

            if normalized_search:
                search_pattern = f"%{normalized_search}%"

                filters.append(
                    or_(
                        User.first_name.ilike(search_pattern),
                        User.last_name.ilike(search_pattern),
                        User.email.ilike(search_pattern),
                    )
                )

        # Filter by role
        if role_id is not None:
            filters.append(User.role_id == role_id)

        # Filter active/inactive users
        if is_active is not None:
            filters.append(User.is_active == is_active)

        # Count query
        count_statement = (
            select(func.count(User.id))
            .select_from(User)
            .where(*filters)
        )

        total = self.db.scalar(count_statement) or 0

        # Secure sorting
        sort_column = self.SORTABLE_COLUMNS.get(
            sort_by,
            User.created_at,
        )

        if sort_order == "asc":
            order_expression = sort_column.asc()
        else:
            order_expression = sort_column.desc()

        offset = (page - 1) * page_size

        # Data query
        statement = (
            select(User)
            .options(selectinload(User.role))
            .where(*filters)
            .order_by(order_expression, User.id.desc())
            .offset(offset)
            .limit(page_size)
        )

        users = self.db.scalars(statement).all()

        return list(users), total



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
