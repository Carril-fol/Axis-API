from ..database.database import Database

from users.entity import UserEntity
from products.entity import ProductEntity
from categories.entity import CategoryEntity
from stock.entity import StockEntity
from companies.entity import CompanyEntity
from roles.entity import RoleEntity
from users_companies.entity import UserCompanyEntity
from permissions.entity import PermissionsEntity

from shared.seeds.permissions_seeder import seed_permissions

def start_server(app):
    db = Database()
    db.initialize()

    seed_permissions()
    app.run(host="0.0.0.0", port=8000, debug=True)