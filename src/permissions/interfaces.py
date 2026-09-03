from abc import ABC, abstractmethod


class IPermissionService(ABC):

    @abstractmethod
    def get_all_permissions(self) -> list[dict]:
        pass

    @abstractmethod
    def create_permission(self, data: dict):
        pass
