from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import connection
from django.core.cache import cache
from app.models import Admin
from app.serializers.Admin_Regist_login_serializers import (
    AdminRegistrationSerializer,
    userLoginSerializer,
    adminLoginSerializer
)
import logging


class RegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Admin.objects.all()
    serializer_class = AdminRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admin, admin_meta, adminhqdiv = serializer.save()

        return Response({
            'admin': {
                'admin_id': admin.admin_id,
                'admin_email': admin.admin_email,
                'username': admin.username,  
                'password': admin.password, 
                'line_manager': admin.line_manager,  
                'status': admin.status,  
                'is_block': admin.is_block,
                'permission_id': admin.permission_id,
                'created_by': admin.created_by,
                'created_date': admin.created_date,
            },
            'admin_meta': {
                'ad_meta_id': admin_meta.ad_meta_id,
                'admin_id': admin.admin_id,
                'address': admin_meta.address,
                'taluka': admin_meta.taluka,
                'district': admin_meta.district,
                'state': admin_meta.state,
                'pin_code': admin_meta.pin_code,
                'geo_location': admin_meta.geo_location,
                'vetzone': admin_meta.vetzone,
                'emp_id': admin_meta.emp_id,
                'mob_number_company': admin_meta.mob_number_company,
                'mob_number_personal': admin_meta.mob_number_personal,

            },
            'admin_hq_div': {
                'admin_hq_div_id': adminhqdiv.admin_hq_div_id,
                'admin_id': admin.admin_id,
                'hq_id': adminhqdiv.hq_id,
                'div_id': adminhqdiv.div_id,
                'sub_division': adminhqdiv.sub_division,
            },
        }, status=status.HTTP_201_CREATED)

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



logger = logging.getLogger(__name__)

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = adminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admin_email = serializer.validated_data['admin_email']
        password = serializer.validated_data['password']

        # Cache keys
        lock_key = f"{admin_email}_lock"
        attempts_key = f"{admin_email}_attempts"
        lock_duration = 3600  # 1 hour in seconds

        # Check if the account is locked
        if cache.get(lock_key):
            return Response({"detail": "Account locked. Please try again later."}, status=403)

        try:
            admin = Admin.objects.get(admin_email=admin_email)

            # Direct password comparison without hashing
            if password != admin.password:
                # Increment failed attempts
                failed_attempts = cache.get(attempts_key, 0) + 1
                cache.set(attempts_key, failed_attempts, timeout=lock_duration)

                # Log failed attempts for debugging
                logger.info(f"Failed attempt #{failed_attempts} for user: {admin_email}")

                if failed_attempts >= 5:
                    # Lock the account
                    cache.set(lock_key, True, timeout=lock_duration)
                    cache.set(attempts_key, 0, timeout=lock_duration)  # Reset attempt count after locking
                    return Response({"detail": "Too many failed attempts. Account locked for 1 hour."}, status=403)
                
                return Response({"detail": "Invalid credentials"}, status=400)

            # Reset failed attempts on successful login
            cache.delete(attempts_key)
            cache.delete(lock_key)

            # Retrieve designation
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.desig_name 
                    FROM admin_roles ar
                    JOIN designations d ON ar.desig_id = d.desig_id
                    WHERE ar.admin_id = %s
                """, [admin.admin_id])
                result = cursor.fetchone()

            if result:
                designation = result[0].strip()
                if designation.lower() != 'admin':
                    return Response({"detail": "Only admin can login here"}, status=403)
            else:
                return Response({"detail": "Designation not found for this admin"}, status=404)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(admin)
            refresh['designation'] = designation
            

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "admin_id": admin.admin_id,
                "designation": designation,
            })

        except Admin.DoesNotExist:
            logger.warning(f"Login attempt with non-existent email: {admin_email}")
            return Response({"detail": "Admin not found"}, status=404)



# class UserLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         admin_email = serializer.validated_data['admin_email']
#         password = serializer.validated_data['password']

#         try:
#             admin = Admin.objects.get(admin_email=admin_email)
            
#             if password != admin.password:
#                 return Response({"detail": "Invalid credentials"}, status=400)

#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT d.desig_name 
#                     FROM admin_roles ar
#                     JOIN designations d ON ar.desig_id = d.desig_id
#                     WHERE ar.admin_id = %s
#                 """, [admin.admin_id])
#                 result = cursor.fetchone()

#             if result:
#                 designation = result[0].strip()

#                 # Ensure only non-admin users can log in here
#                 if designation.lower() == 'admin':
#                     return Response({"detail": "Admin users cannot login here"}, status=403)
#             else:
#                 return Response({"detail": "Designation not found for this admin"}, status=404)

#             # Generate token for successful user login
#             refresh = RefreshToken.for_user(admin)
#             return Response({
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#                 "admin_id": admin.admin_id,
#                 "designation": designation,
#             })

#         except Admin.DoesNotExist:
#             return Response({"detail": "Admin not found"}, status=404)


logger = logging.getLogger(__name__)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = userLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admin_email = serializer.validated_data['admin_email']
        password = serializer.validated_data['password']

        # Cache keys
        lock_key = f"{admin_email}_lock"
        attempts_key = f"{admin_email}_attempts"
        lock_duration = 3600  # 1 hour in seconds

        # Check if the account is locked
        if cache.get(lock_key):
            return Response({"detail": "Account locked. Please try again later."}, status=403)

        try:
            admin = Admin.objects.get(admin_email=admin_email)

            # Direct password comparison without hashing
            if password != admin.password:
                # Increment failed attempts
                failed_attempts = cache.get(attempts_key, 0) + 1
                cache.set(attempts_key, failed_attempts, timeout=lock_duration)

                # Log failed attempts for debugging
                logger.info(f"Failed attempt #{failed_attempts} for user: {admin_email}")

                if failed_attempts >= 5:
                    # Lock the account
                    cache.set(lock_key, True, timeout=lock_duration)
                    cache.set(attempts_key, 0, timeout=lock_duration)  # Reset attempt count after locking
                    return Response({"detail": "Too many failed attempts. Account locked for 1 hour."}, status=403)
                
                return Response({"detail": "Invalid credentials"}, status=400)

            # Reset failed attempts on successful login
            cache.delete(attempts_key)
            cache.delete(lock_key)

            # Retrieve designation
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT d.desig_name 
                    FROM admin_roles ar
                    JOIN designations d ON ar.desig_id = d.desig_id
                    WHERE ar.admin_id = %s
                """, [admin.admin_id])
                result = cursor.fetchone()

            if result:
                designation = result[0].strip()
                # Ensure only non-admin users can log in here
                if designation.lower() == 'admin':
                    return Response({"detail": "Admin users cannot login here"}, status=403)
            else:
                return Response({"detail": "Designation not found for this admin"}, status=404)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(admin)
            refresh['designation'] = designation

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "admin_id": admin.admin_id,
                "designation": designation,
            })

        except Admin.DoesNotExist:
            logger.warning(f"Login attempt with non-existent email: {admin_email}")
            return Response({"detail": "Admin not found"}, status=404)
