from abc import ABC, abstractmethod


class IRolePermissionService(ABC):

    @abstractmethod
    def assign_role_permission(self, data: dict, company_id: int):
        pass

    @abstractmethod
    def grant_all_permissions(self, role_id: int) -> None:
        pass

    @abstractmethod
    def update_role_permission(self, id: int, data: dict, company_id: int):
        pass

    @abstractmethod
    def list_permissions_by_role_id(self, role_id: int, company_id: int) -> list[str]:
        pass

    @abstractmethod
    def revoke_permission(self, role_id: int, permission_id: int, company_id: int):
        pass
