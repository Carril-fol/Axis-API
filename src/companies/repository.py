from shared.database.base_repository import BaseRepository
from .entity import CompanyEntity


class CompanyRepository(BaseRepository):
    
    def __init__(self):
        super().__init__(CompanyEntity)
