from shared.service import BaseService

from roles.interfaces import IRoleService

from .interfaces import ICompanyService
from .repository import CompanyRepository
from .model import CreateCompanyModel, DetailCompanyModel
from .entity import CompanyEntity
from .exceptions import CompanyNotFound, CompanyInsufficientRolePrivileges


class CompanyService(ICompanyService, BaseService):

    def __init__(
            self, 
            company_repository: CompanyRepository, 
            role_service: IRoleService, 
        ):
        self.company_repository = company_repository
        self._role_service = role_service

    def _is_user_owner_of_company(self, requesting_role_id: int, company_id: int) -> bool:
        requesting_role = self._role_service.get_role_by_id(requesting_role_id)
        if requesting_role["company_id"] != company_id:
            return False
        
        if requesting_role["name"] == "OWNER" and requesting_role["company_id"] == company_id:
            return True
        
        return False
    
    def _get_company_or_raise(self, company_id: int) -> CompanyEntity:
        company = self.company_repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFound()
        return company

    def create_company(self, data: dict) -> CompanyEntity:
        company_dump = CreateCompanyModel.model_validate(data).model_dump()
        return self.company_repository.create(CompanyEntity(**company_dump))

    def update_company(self, company_id: int, data: dict, requesting_role_id: int) -> CompanyEntity:
        if not self._is_user_owner_of_company(requesting_role_id, company_id):
            raise CompanyInsufficientRolePrivileges()
        
        company = self._get_company_or_raise(company_id)
        company_updated = self._update_instance_entity(data, company)
        return self.company_repository.update(company_updated)

    def detail_company(self, company_id: int, requesting_role_id: int) -> dict:
        if not self._is_user_owner_of_company(requesting_role_id, company_id):
            raise CompanyInsufficientRolePrivileges()

        company = self._get_company_or_raise(company_id)
        return DetailCompanyModel.model_validate(company).model_dump()
