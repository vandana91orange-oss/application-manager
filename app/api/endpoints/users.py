from app.core.security import hash_password, verify_password
from app.models.users import User
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    CurrentUserResponse,
    ChangePasswordRequest, 
    MessageResponse
)

from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.dependencies.auth import UserRole, require_roles, get_current_user


router=APIRouter(
    prefix="/users",
    tags=["Users"]
)



def get_service(
    db:Session=Depends(get_db)
):

    return UserService(
        UserRepository(db)
    )


@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    user:UserCreate,
    service=Depends(get_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN

        )
    )
):

    return service.create(user)


@router.get(
    "",
    response_model=list[UserResponse]
)
def users(
    service=Depends(get_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )
):

    return service.get_all()


@router.get(
    "/{id}",
    response_model=UserResponse
)
def user(
    id:int,
    service=Depends(get_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER,
            UserRole.EMPLOYEE,
            UserRole.VIEWER,

        )
    )
):

    return service.get_one(id)


@router.put(
    "/{id}",
    response_model=UserResponse
)
def update(
    id:int,
    data:UserUpdate,
    service=Depends(get_service),
    current_user=Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.MANAGER

        )
    )
):

    return service.update(
        id,
        data
    )


@router.delete(
    "/{id}",
)
def delete(
    id:int,
    current_user=Depends(
        require_roles(
            UserRole.ADMIN
        )
    ),
    service=Depends(get_service)
):

    service.delete(id)

    return {
        "message":"User deleted"
    }


@router.get(
    "me",
    response_model=CurrentUserResponse
)
def get_current_user_details(
    current_user: User = Depends(get_current_user)
):
    return CurrentUserResponse(
        id=int(current_user.id),
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        role=current_user.role.name
    )


@router.patch(
    "/change-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    """
    Change the password of the currently authenticated user.
    """

    # Verify the user's existing password
    if not verify_password(
        payload.current_password,
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    # Prevent reuse of the current password
    if verify_password(
        payload.new_password,
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current password.",
        )

    try:
        current_user.hashed_password = hash_password(
            payload.new_password
        )

        db.add(current_user)
        db.commit()

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update password.",
        )

    return MessageResponse(
        message="Password changed successfully."
    )
