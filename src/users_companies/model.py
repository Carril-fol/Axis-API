from datetime import datetime

from pydantic import BaseModel, Field

from companies.model import CreateCompanyInput
from users.model import RegisterInput, CreateUserModel


class BaseUsersCompaniesModel(BaseModel):
    user_id: int
    role_id: int
    company_id: int

    
class CreateUserCompanyModel(BaseUsersCompaniesModel):
    pass


class DetailUsersCompaniesModel(BaseUsersCompaniesModel):
    pass


class UserFromCompanyModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    date_creation: datetime
    role_id: int


class UsersFromCompanyOutput(BaseModel):
    users: list[UserFromCompanyModel]


class RegisterWithCompanyInput(BaseModel):
    user: RegisterInput = Field(..., description="Datos del usuario OWNER")
    company: CreateCompanyInput = Field(..., description="Datos de la empresa")


class RegisterInputFromCompany(RegisterInput):
    role_id: int = Field(..., description="Role to assign to the new user")


class CreateUserFromCompany(CreateUserModel):
    pass