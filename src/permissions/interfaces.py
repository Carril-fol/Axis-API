from abc import ABC, abstractmethod


class IPermissionService(ABC):

    @abstractmethod
    def get_permission_by_name(self, name: str) -> dict:
        pass

    @abstractmethod
    def get_all_permissions(self) -> list[dict]:
        pass

    @abstractmethod
    def create_permission(self, data: dict):
        pass
