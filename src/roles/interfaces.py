from abc import ABC, abstractmethod

from .entity import RoleEntity
from .model import DetailRoleModel, RoleListDetail


class IRoleService(ABC):

    @abstractmethod
    def create_role(self, data: dict, company_id: int) -> RoleEntity:
        pass

    @abstractmethod
    def get_roles_from_company(self, company_id: int, page: int, per_page: int) -> RoleListDetail:
        pass

    @abstractmethod
    def get_role_by_id(self, id: int) -> DetailRoleModel:
        pass

    @abstractmethod
    def delete_soft_rol(self, id: int, data: dict):
        pass

    @abstractmethod
    def ensure_default_role(self, company_id: int) -> int:
        pass

    @abstractmethod
    def ensure_owner_role(self, company_id: int) -> int:
        pass

    @abstractmethod
    def update_role(self, id: int, data: dict):
        pass

    @abstractmethod
    def is_role_owner(self, role_id: int) -> bool:
        pass