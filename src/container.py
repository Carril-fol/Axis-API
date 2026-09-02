from categories.repository import CategoryRepository
from companies.repository import CompanyRepository
from permissions.repository import PermissionRepository
from products.repository import ProductRepository
from role_permissions.repository import RolePermissionsRepository
from roles.repository import RoleRepository
from stock.repository import StockRepository
from users.repository import UserRepository
from users_companies.repository import UserCompanyRepository

from auth.service import AuthService
from categories.service import CategoryService
from companies.service import CompanyService
from permissions.service import PermissionService
from products.service import ProductService
from role_permissions.service import RolePermissionService
from roles.membership_service import RoleMembershipService
from roles.service import RoleService
from stock.service import StockService
from users.orchestrator import UserRegistrationOrchestrator
from users.service import UserService
from users_companies.service import UserCompanyService


category_repository = CategoryRepository()
company_repository = CompanyRepository()
permission_repository = PermissionRepository()
product_repository = ProductRepository()
stock_repository = StockRepository()
role_permissions_repository = RolePermissionsRepository()
role_repository = RoleRepository()
user_repository = UserRepository()
user_company_repository = UserCompanyRepository()


permission_service = PermissionService(permission_repository)
stock_service = StockService(stock_repository)
role_service = RoleService(role_repository)
user_service = UserService(user_repository)


product_service = ProductService(product_repository, stock_service)
category_service = CategoryService(category_repository, product_service)
company_service = CompanyService(company_repository, role_service)
role_permission_service = RolePermissionService(
    role_permissions_repository,
    role_service,
    permission_service,
)
auth_service = AuthService(user_service)
user_company_service = UserCompanyService(user_service, role_service, user_company_repository)


role_membership_service = RoleMembershipService(role_service, user_company_service)
user_registration_orchestrator = UserRegistrationOrchestrator(
    user_service,
    company_service,
    role_service,
    role_permission_service,
    user_company_service,
)
