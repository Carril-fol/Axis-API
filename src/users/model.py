from datetime import datetime
from argon2 import PasswordHasher
from pydantic import BaseModel, Field, field_validator, model_validator

from .exceptions import PasswordDontMatch

ph = PasswordHasher()


class BaseUserModel(BaseModel):
    first_name: str = Field(..., description='First name of the user')
    last_name: str = Field(..., description='Last name of the user')
    email: str = Field(..., description='Email of the user')
    date_creation: datetime = Field(default_factory=datetime.now, description="Date of the creation user")

    @field_validator("first_name", "last_name", mode='before')
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


class CreateUserModel(BaseUserModel):
    password: str = Field(...)

    @field_validator('password', mode='before')
    @classmethod
    def hash_password(cls, value):
        return ph.hash(value)


class UpdateUserInput(BaseModel):
    first_name: str | None = Field(default=None, description='First name of the user')
    last_name: str | None = Field(default=None, description='Last name of the user')
    email: str | None = Field(default=None, description='Email of the user')
    date_creation: datetime | None = Field(default=None, description="Date of the creation user")
    password: str | None = Field(default=None, description="New password. Optional: omit it to keep the current one", examples=["secret123"])
    confirm_password: str | None = Field(default=None, description="Must match password when a new one is sent", examples=["secret123"])

    @field_validator("first_name", "last_name", mode='before')
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @model_validator(mode='before')
    @classmethod
    def check_passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise PasswordDontMatch()
        return values


class UpdateUserModel(BaseModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    password: str | None = Field(default=None)

    @field_validator('password', mode='before')
    @classmethod
    def hash_password(cls, value):
        if value:
            return ph.hash(value)
        return value


class DetailUserModel(BaseUserModel):
    id: int = Field(..., description='ID of the user')
    date_creation: datetime = Field(..., description='Creation date of the user')
