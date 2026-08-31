from datetime import datetime
from typing import Optional
from argon2 import PasswordHasher
from pydantic import BaseModel, Field, field_validator, model_validator

from .exceptions import PasswordDontMatch

from auth.model import RegisterInput

ph = PasswordHasher()


class BaseUserModel(BaseModel):
    first_name: str = Field(default=None, description='First name of the user')
    last_name: str = Field(default=None, description='Last name of the user')
    email: str = Field(default=None, description='Email of the user')
    date_creation: datetime = Field(default_factory=datetime.now, description="Date of the creation user")

    @field_validator("first_name", "last_name", mode='before',)
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    

class CreateUserModel(BaseUserModel):
    password: str = Field(...)

    @field_validator('password', mode='before')
    def hash_password(cls, value):
        return ph.hash(value)


class UpdateUserInput(BaseUserModel):
    password: str = Field(default=None)
    confirm_password: str = Field(default=None)

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise PasswordDontMatch()
        return values


class UpdateUserOutput(BaseModel):
    msg: str = Field(..., examples=["User updated successful"])


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    @field_validator('password', mode='before')
    def hash_password(cls, value):
        if value:
            return ph.hash(value)
        return value


class DetailUserModel(BaseUserModel):
    id: int = Field(..., description='ID of the user')
    date_creation: datetime = Field(..., description='Creation date of the user')


class RegisterInputFromCompany(RegisterInput):
    role_id: int = Field(..., description="Role to assign to the new user")


class CreateUserFromCompany(CreateUserModel):
    pass


class RegisterOutput(BaseModel):
    msg: str = Field(..., examples=["Register successful"])


class DeleteUserOutput(BaseModel):
    msg: str = Field(..., examples=["User deleted successfully"])


class ErrorOutput(BaseModel):
    error: str
    
