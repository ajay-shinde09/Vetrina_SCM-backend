from rest_framework.permissions import BasePermission
from django.db import connection

from .models import Customer

def check_designation(user, designation_name):
    if not user:
        return False
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT d.desig_name
            FROM admin_roles ar
            JOIN designations d ON ar.desig_id = d.desig_id
            WHERE ar.admin_id = %s
        ''', [user.admin_id])
        designation = cursor.fetchone()
    return designation and designation[0] == designation_name

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "Admin")

class IsNonAdminUser(BasePermission):
    def has_permission(self, request, view):
        return not check_designation(request.user, "Admin")

class IsGeneralManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "GM (General Manager)")

class IsNationalSalesManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "NSM (National Sales Manager)")

class IsZonalSalesManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "ZSM (Zonal Sales Manager)")

class IsAreaSalesManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "ASM (Area Sales Manager)")

class IsVeterinarySalesOfficer(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "VSO (Veterinary Sales Officer)")

class IsVetZoneOperationExecutive(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "VOE (VetZone Operation Executive)")

class IsCommercialOperationManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "COM  (Commercial Operation Manager)")

class IsFinanceManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "FM (Finance Manager)")

class IsAccountManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "AM (Account Manager)")

class IsChiefExecutiveOfficer(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "CEO (Chief Executive Officer)")

class IsCustomerRelationshipManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "CRM (Customer Relationship Manager)")

class IsVetZoneSupervisor(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "VS (VetZone Supervisor)")

class IsCommercialOperationExecutive(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "COE (Commercial Operation Executive)")

class IsSalesHead(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "SH (Sales Head)")

class IsHeadOfDepartment(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "HOD")

class IsBusinessDevelopmentManager(BasePermission):
    def has_permission(self, request, view):
        return check_designation(request.user, "BDM (Business Development Manager)")
    
# def check_customer_role(user, role_name):
#     if not user:
#         return False
#     with connection.cursor() as cursor:
#         cursor.execute('''
#             SELECT cr.role_name
#             FROM customer_roles cr
#             JOIN customer c ON c.role = cr.cust_role_id
#             WHERE c.customer_id = %s
#         ''', [user.customer_id])
#         role = cursor.fetchone()
#     return role and role[0] == role_name

# # Base permission for customers
# class IsCustomer(BasePermission):
#     def has_permission(self, request, view):
#         if not request.user:
#             return False
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT role
#                 FROM customer
#                 WHERE customer_id = %s
#             """, [request.user.customer_id])
#             role = cursor.fetchone()
#         return role is not None
def check_customer_role(user, role_name):
    if not user or not hasattr(user, 'customer_id'):  # Ensure user is a Customer
        return False
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT cr.role_name
            FROM customer_roles cr
            JOIN customer c ON c.role = cr.cust_role_id
            WHERE c.customer_id = %s
        ''', [user.customer_id])
        role = cursor.fetchone()
    return role and role[0] == role_name

# Base permission for customers
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer_id')


# Specific permissions for each role
class IsCnF(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "C&F")

class IsStockiest(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Stockiest")

class IsKeyAccount(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Key Account")

class IsRetailer(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Retailer")

class IsPetShop(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Pet Shop")

class IsFarmer(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Farmer")

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Doctor")

class IsLSS(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "LSS")

class IsPetOwner(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "Pet Owner")

class IsVetZone(BasePermission):
    def has_permission(self, request, view):
        return check_customer_role(request.user, "VetZone")