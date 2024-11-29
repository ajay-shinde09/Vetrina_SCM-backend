# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.throttling import UserRateThrottle 
# from app.serializers.Cust_Regist_login_serializers import CustomerLoginSerializer
# from rest_framework.permissions import AllowAny

# class CustomerLoginView(APIView):
#     permission_classes = [AllowAny]
#     serializer_class = CustomerLoginSerializer  # Specify the serializer class
#     throttle_classes = [UserRateThrottle] 

#     def post(self, request, *args, **kwargs):
#         serializer = CustomerLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             customer = serializer.validated_data['customer']
            
#             # Generate custom JWT Token using 'customer_id' instead of 'id'
#             refresh = RefreshToken()
#             refresh['customer_id'] = customer.customer_id
            
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token)
#             }, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from django.db import connection
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
# from rest_framework_simplejwt.tokens import RefreshToken
# from app.serializers.Cust_Regist_login_serializers import CustomerauthLoginSerializer

# from rest_framework_simplejwt.tokens import RefreshToken

# # class CustomerauthLoginView(APIView):
# #     def post(self, request, *args, **kwargs):
# #         permission_classes = [AllowAny]
# #         serializer = CustomerauthLoginSerializer(data=request.data)
# #         if serializer.is_valid():
# #             email = serializer.validated_data['email']
# #             password = serializer.validated_data['password']

# #             # Use raw SQL to fetch customer and role details
# #             with connection.cursor() as cursor:
# #                 query = """
# #                 SELECT c.customer_id, c.name, c.email, c.role, r.role_name
# #                 FROM customer c
# #                 JOIN customer_roles r ON c.role = r.cust_role_id
# #                 WHERE c.email = %s AND c.password = %s AND c.is_block = 'N'
# #                 """
# #                 cursor.execute(query, [email, password])
# #                 customer = cursor.fetchone()

# #             if customer:
# #                 # Generate JWT tokens without relying on a user object
# #                 refresh = RefreshToken()
# #                 refresh['role'] = customer[3]  # Adding role to token
# #                 refresh['customer_id'] = customer[0]
# #                 access = refresh.access_token

# #                 return Response({
# #                     'refresh': str(refresh),
# #                     'access': str(access),
# #                     'customer_id': customer[0],
# #                     'name': customer[1],
# #                     'email': customer[2],
# #                     'role_name': customer[4],
# #                 }, status=HTTP_200_OK)
# #             return Response({'error': 'Invalid credentials or account blocked'}, status=HTTP_401_UNAUTHORIZED)
# #         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
# class CustomerauthLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = CustomerauthLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             # Use raw SQL to fetch customer and role details
#             with connection.cursor() as cursor:
#                 query = """
#                 SELECT c.customer_id, c.name, c.email, c.role, r.role_name
#                 FROM customer c
#                 JOIN customer_roles r ON c.role = r.cust_role_id
#                 WHERE c.email = %s AND c.password = %s AND c.is_block = 'N'
#                 """
#                 cursor.execute(query, [email, password])
#                 customer = cursor.fetchone()

#             if customer:
#                 # Generate JWT tokens
#                 refresh = RefreshToken()
#                 refresh['user_id'] = customer[0]  # Use 'user_id' to align with SimpleJWT expectations
#                 refresh['role'] = customer[3]
#                 access = refresh.access_token

#                 return Response({
#                     'refresh': str(refresh),
#                     'access': str(access),
#                     'customer_id': customer[0],
#                     'name': customer[1],
#                     'email': customer[2],
#                     'role_name': customer[4],
#                 }, status=HTTP_200_OK)

#             return Response({'error': 'Invalid credentials or account blocked'}, status=HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# Import necessary modules and classes from Django REST framework
from rest_framework import status  # For HTTP status codes
from rest_framework.response import Response  # To send HTTP responses
from rest_framework.views import APIView  # Base class for defining API views
from rest_framework_simplejwt.tokens import RefreshToken  # For generating JWT tokens
from rest_framework.throttling import UserRateThrottle  # To limit the request rate for a user
from app.serializers.Cust_Regist_login_serializers import CustomerLoginSerializer  # Custom serializer for customer login
from rest_framework.permissions import AllowAny  # Permission class to allow unrestricted access

# Define a view for customer login using Django REST framework's APIView
class CustomerLoginView(APIView):
    permission_classes = [AllowAny]  # Allow access to this view without authentication
    serializer_class = CustomerLoginSerializer  # Specify the serializer class for validating login data
    throttle_classes = [UserRateThrottle]  # Apply throttling to limit the rate of requests

    def post(self, request, *args, **kwargs):
        # Instantiate the serializer with the request data
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():  # Check if the serializer data is valid
            customer = serializer.validated_data['customer']  # Extract the validated customer object
            
            # Generate a new JWT refresh token
            refresh = RefreshToken()
            refresh['customer_id'] = customer.customer_id  # Add 'customer_id' to the token payload
            
            # Return the generated tokens in the response
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        # If serializer validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Import additional modules for handling raw SQL and JWT tokens
from django.db import connection  # For executing raw SQL queries
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED  # HTTP status codes
from app.serializers.Cust_Regist_login_serializers import CustomerauthLoginSerializer  # Serializer for authentication login

# Define another view for customer authentication
class CustomerauthLoginView(APIView):
    permission_classes = [AllowAny]  # Allow unrestricted access to this view

    def post(self, request, *args, **kwargs):
        # Instantiate the serializer with the request data
        serializer = CustomerauthLoginSerializer(data=request.data)
        if serializer.is_valid():  # Check if the serializer data is valid
            email = serializer.validated_data['email']  # Extract the validated email
            password = serializer.validated_data['password']  # Extract the validated password

            # Use raw SQL to fetch customer and role details from the database
            with connection.cursor() as cursor:
                query = """
                SELECT c.customer_id, c.name, c.email, c.role, r.role_name
                FROM customer c
                JOIN customer_roles r ON c.role = r.cust_role_id
                WHERE c.email = %s AND c.password = %s AND c.is_block = 'N'
                """
                cursor.execute(query, [email, password])  # Execute the SQL query with parameters
                customer = cursor.fetchone()  # Fetch a single record from the query result

            if customer:  # Check if a customer record was found
                # Generate a new JWT refresh token
                refresh = RefreshToken()
                refresh['user_id'] = customer[0]  # Add 'customer_id' to the token payload
                refresh['role'] = customer[3]  # Add the customer role to the token payload
                refresh['customer_id'] = customer[0]  # Add 'customer_id' to the token payload
                refresh['role_name'] = customer[4]  # Add the customer role to the token payload
                access = refresh.access_token  # Generate the access token

                # Return the generated tokens and customer details in the response
                return Response({
                    'refresh': str(refresh),
                    'access': str(access),
                    'customer_id': customer[0],
                    'name': customer[1],
                    'email': customer[2],
                    'role_name': customer[4],
                }, status=HTTP_200_OK)

            # If customer not found, return an error message
            return Response({'error': 'Invalid credentials or account blocked'}, status=HTTP_401_UNAUTHORIZED)
        
        # If serializer validation fails, return the errors
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
