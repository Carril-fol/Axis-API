from abc import ABC, abstractmethod

from .entity import CompanyEntity


class ICompanyService(ABC):

    @abstractmethod
    def create_company(self, data: dict) -> CompanyEntity:
        pass

    @abstractmethod
    def update_company(self, company_id: int, data: dict, requesting_role_id: int) -> CompanyEntity:
        pass

    @abstractmethod
    def detail_company(self, company_id: int, requesting_role_id: int) -> dict:
        pass
