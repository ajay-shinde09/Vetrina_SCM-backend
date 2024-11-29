from django.contrib.auth.backends import BaseBackend
from .models import Admin, Customer 
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import connection

class CustomAdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = Admin.objects.get(admin_email=username)
            # Use check_password if passwords are hashed; otherwise, continue
            if admin.password == password:
                return admin
        except Admin.DoesNotExist:
            return None

    def get_user(self, admin_id):
        try:
            return Admin.objects.get(admin_id=admin_id)
        except Admin.DoesNotExist:
            return None

    def create_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        refresh.payload['user_id'] = user.admin_id
        return str(refresh)

# class CustomCustomerBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             customer = Customer.objects.get(email=username)  # Assuming email field in Customer model
#             if customer.password == password:
#                 return customer
#         except Customer.DoesNotExist:
#             return None

#     def get_user(self, customer_id):
#         try:
#             return Customer.objects.get(customer_id=customer_id)
#         except Customer.DoesNotExist:
#             return None

#     def create_jwt(self, user):
#         refresh = RefreshToken.for_user(user)
#         refresh.payload['customer_id'] = user.id
#         refresh.payload['role'] = user.role  # Assuming a role field exists in the Customer model
#         return str(refresh)
class CustomCustomerBackend(BaseBackend):
    def get_user(self, customer_id):
        try:
            return Customer.objects.get(customer_id=customer_id)  # Use correct field for lookup
        except Customer.DoesNotExist:
            return None
        
    def create_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['user_id'] = user.id  # Django expects 'user_id' for authentication
        refresh['role'] = user.role
        refresh['role_name'] = user.role_name
        return str(refresh.access_token)