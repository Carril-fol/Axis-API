from abc import ABC, abstractmethod

from .entity import UserCompanyEntity

class IUserCompanyService(ABC):
    
    @abstractmethod
    def create_user_for_company(self, data: dict, company_id: int) -> None:
        pass
    
    @abstractmethod
    def update_user_from_company(self, user_id: int, data: dict, requesting_user_id: int):
        pass
    
    @abstractmethod
    def delete_user_from_company(self, user_id: int, requesting_user_id: int):
        pass
    
    @abstractmethod
    def get_users_from_company(self, company_id: int) -> list[dict]:
        pass

    @abstractmethod
    def create_membership(self, user_id: int, role_id: int, company_id: int) -> UserCompanyEntity:
        pass

    @abstractmethod
    def get_membership_with_permissions(self, user_id: int) -> tuple[UserCompanyEntity | None, set[str]]:
        pass

    @abstractmethod
    def get_membership_by_user_id(self, user_id: int) -> UserCompanyEntity | None:
        pass

    @abstractmethod
    def get_memberships_by_role_id(self, role_id: int) -> list[UserCompanyEntity]:
        pass

    @abstractmethod
    def update_membership(self, membership: UserCompanyEntity) -> UserCompanyEntity:
        pass
