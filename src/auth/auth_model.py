from pydantic import BaseModel, Field, field_validator, model_validator

from .exceptions import PasswordDontMatch, EmailInvalidFormat
from companies.company_model import CreateCompanyInput


class LoginInput(BaseModel):
    email: str = Field(..., description="Email from user", examples=["example@example.com"])
    password: str = Field(..., min_length=1, description="Password in text plain")


class RegisterInput(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        if values.get('password') != values.get('confirm_password'):
            raise PasswordDontMatch()
        return values
    
    @field_validator("email")
    def validate_email_format(cls, value):
        if "@" not in value or "." not in value:
            raise EmailInvalidFormat()
        return value


class RegisterWithCompanyInput(BaseModel):
    user: RegisterInput = Field(..., description="Datos del usuario OWNER")
    company: CreateCompanyInput = Field(..., description="Datos de la empresa")


class AuthOutput(BaseModel):
    msg: str = Field(..., examples=["Register successful", "Error auth"])
    access_token: str | None = Field(
        default=None,
        description="JWT de acceso. Tambien se setea como cookie HttpOnly."
    )