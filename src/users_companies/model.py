from datetime import datetime

from pydantic import BaseModel, Field

from auth.model import RegisterInput


class BaseUsersCompaniesModel(BaseModel):
    user_id: int = Field(..., description="ID of the user", examples=[2])
    role_id: int = Field(..., description="ID of the role the user has in the company", examples=[2])
    company_id: int = Field(..., description="ID of the company", examples=[1])

    
class CreateUserCompanyModel(BaseUsersCompaniesModel):
    pass


class UserFromCompanyModel(BaseModel):
    id: int = Field(..., description="ID of the user", examples=[2])
    first_name: str = Field(..., description="First name of the user", examples=["ANA"])
    last_name: str = Field(..., description="Last name of the user", examples=["LOPEZ"])
    email: str = Field(..., description="Email of the user", examples=["ana@acme.com"])
    date_creation: datetime = Field(..., description="When the user was created")
    role_id: int = Field(..., description="ID of the role the user has in this company", examples=[2])


class UsersFromCompanyOutput(BaseModel):
    users: list[UserFromCompanyModel] = Field(..., description="Every user that belongs to the company, with their role")


class RegisterInputFromCompany(RegisterInput):
    role_id: int = Field(..., description="Role to assign to the new user")
