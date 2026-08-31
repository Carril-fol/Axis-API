from math import ceil

from shared.service import BaseService

from .interfaces import IRoleService
from .repository import RoleRepository
from .entity import RoleEntity
from .model import (
    CreateRoleModel, 
    DetailRoleModel, 
    RoleListDetail, 
    CreateRoleInput,
    UpdateRoleInput
)
from .exceptions import (
    RoleNotFound, 
    RoleIsAlreadyInactive, 
    RoleNameReserved
)


RESERVED_ROLE_NAME = "DEFAULT"
OWNER_ROLE_NAME = "OWNER"


class RoleService(IRoleService, BaseService):
    
    def __init__(self, role_repository: RoleRepository):
        self._role_repository = role_repository        

    def _get_role_by_or_raise(self, id: int):
        role = self._role_repository.get_by_id(id)
        if not role:
            raise RoleNotFound()
        return role
    
    def create_role(self, data: dict, company_id: int) -> RoleEntity:
        if data["name"].upper() == RESERVED_ROLE_NAME:
            raise RoleNameReserved()

        data["company_id"] = company_id
        role_data_validated = CreateRoleModel.model_validate(data).model_dump()

        role_entity = RoleEntity(**role_data_validated)
        return self._role_repository.create(role_entity)
    
    def get_roles_from_company(self, company_id: int, page: int, per_page: int) -> RoleListDetail:        
        roles_raw, total = self._role_repository.get_roles_from_company_id(company_id, page, per_page)
        roles_formatted: list[DetailRoleModel] = [DetailRoleModel.model_validate(rol).model_dump() for rol in roles_raw]
        return RoleListDetail(
            data=roles_formatted,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=ceil(total / per_page) if total > 0 else 1
        )
    
    def get_role_by_id(self, id: int) -> DetailRoleModel:
        role = self._get_role_by_or_raise(id)
        return DetailRoleModel.model_validate(role).model_dump()
    
    def is_role_owner(self, id: int) -> bool:
        role = self._get_role_by_or_raise(id)
        return role.name == OWNER_ROLE_NAME

    def delete_soft_rol(self, id: int, data: dict):
        role = self._get_role_by_or_raise(id)
        
        if role.status == "INACTIVE":
            raise RoleIsAlreadyInactive()

        role_updated = self._update_instance_entity(data, role)
        return self._role_repository.update(role_updated)

    def _ensure_role(self, name: str, company_id: int) -> int:
        existing = self._role_repository.get_role_by_name(name, company_id)

        if existing:
            if existing.status != "ACTIVE":
                reactivated = self._update_instance_entity({"status": "ACTIVE"}, existing)
                return self._role_repository.update(reactivated).id
            return existing.id

        data = {"name": name, "company_id": company_id, "status": "ACTIVE"}
        role_entity = RoleEntity(**data)
        return self._role_repository.create(role_entity).id

    def ensure_default_role(self, company_id: int) -> int:
        return self._ensure_role(RESERVED_ROLE_NAME, company_id)

    def ensure_owner_role(self, company_id: int) -> int:
        return self._ensure_role(OWNER_ROLE_NAME, company_id)

    def update_role(self, id: int, data: dict):
        role = self._get_role_by_or_raise(id)
        role_to_updated = self._update_instance_entity(data, role)
        return self._role_repository.update(role_to_updated)
