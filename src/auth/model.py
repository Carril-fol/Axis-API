from pydantic import BaseModel, Field, field_validator, model_validator

from .exceptions import PasswordDontMatch, EmailInvalidFormat
from companies.model import CreateCompanyInput


class LoginInput(BaseModel):
    email: str = Field(..., description="Email of the registered user", examples=["owner@acme.com"])
    password: str = Field(..., min_length=1, description="Plain text password, checked against the stored hash", examples=["secret123"])


class RegisterInput(BaseModel):
    first_name: str = Field(..., description="First name of the user", examples=["Folco"])
    last_name: str = Field(..., description="Last name of the user", examples=["Carril"])
    email: str = Field(..., description="Email of the user, must be unique", examples=["owner@acme.com"])
    password: str = Field(..., description="Plain text password, hashed with argon2 before it is stored", examples=["secret123"])
    confirm_password: str = Field(..., description="Must match password or the request is rejected", examples=["secret123"])

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
    user: RegisterInput = Field(..., description="OWNER user data")
    company: CreateCompanyInput = Field(..., description="Company data")


class AuthOutput(BaseModel):
    msg: str = Field(..., description="Result of the operation", examples=["Register successful", "Error auth"])
    access_token: str | None = Field(
        default=None,
        description="JWT de acceso. Tambien se setea como cookie HttpOnly."
    )
    refresh_token: str | None = Field(
        default=None,
        description="JWT de refresco. Solo lo devuelve /refresh. Tambien se setea como cookie HttpOnly."
    )
