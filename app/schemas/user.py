from pydantic import BaseModel, EmailStr
from datetime import datetime


import re

from pydantic import BaseModel, EmailStr, field_validator, model_validator, Field


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role_id: int

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not (2 <= len(value) <= 50):
            raise ValueError("Must be between 2 and 50 characters.")

        if not re.fullmatch(r"[A-Za-z\s'-]+", value):
            raise ValueError(
                "Only letters, spaces, hyphens, and apostrophes are allowed."
            )

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> EmailStr:
        return value.lower().strip()


    @field_validator("role_id")
    @classmethod
    def validate_role_id(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Role ID must be a positive integer.")
        return value


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    role_id: int | None = None
    is_active: bool | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not (2 <= len(value) <= 50):
            raise ValueError("Must be between 2 and 50 characters.")

        if not re.fullmatch(r"[A-Za-z\s'-]+", value):
            raise ValueError(
                "Only letters, spaces, hyphens, and apostrophes are allowed."
            )

        return value

    @field_validator("role_id")
    @classmethod
    def validate_role_id(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            raise ValueError("Role ID must be a positive integer.")
        return value


class RoleResponse(BaseModel):

    id:int
    name:str

    class Config:
        from_attributes=True



class UserResponse(BaseModel):

    id:int
    first_name:str
    last_name:str
    email:str
    is_active:bool
    role:RoleResponse | None

    created_at:datetime

    class Config:
        from_attributes=True


class CurrentUserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role: str

    class Config:
        from_attributes = True



class ChangePasswordRequest(BaseModel):
    current_password: str = Field(
        ...,
        min_length=1,
        examples=["OldPassword@123"],
    )

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["NewPassword@456"],
    )

    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["NewPassword@456"],
    )

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.new_password != self.confirm_password:
            raise ValueError(
                "New password and confirm password do not match."
            )

        if self.current_password == self.new_password:
            raise ValueError(
                "New password cannot be the same as the current password."
            )

        return self


class MessageResponse(BaseModel):
    message: str
