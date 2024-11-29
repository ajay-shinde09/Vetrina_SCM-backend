# from django.http import JsonResponse
# from django.views import View
# from django.db import connection
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from datetime import datetime
# import json

# class AddToCart(View):
#     @method_decorator(csrf_exempt)  # Disables CSRF for testing; remove in production if unnecessary
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get_user_from_token(self, request):
#         """
#         Extracts user_id and user_role from the access token in the Authorization header.
#         """
#         auth = JWTAuthentication()
#         try:
#             # Extract token from Authorization header
#             token = request.headers.get('Authorization', '').split(' ')[1]
#             validated_token = auth.get_validated_token(token)
#             user_id = validated_token.get('customer_id')
#             user_role = validated_token.get('role_name')
#             #user_role = request.user('role_name')
#             if not user_id or not user_role:
#                 return None, None
#             return user_id, user_role

#         except (InvalidToken, TokenError, IndexError):
#             return None, None

#     def post(self, request, *args, **kwargs):
#         try:
#             # Get user_id and user_role from the JWT token
#             user_id, user_role = self.get_user_from_token(request)
#             if not user_id or not user_role:
#                 return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

#             # Parse the incoming JSON payload
#             body = json.loads(request.body)
#             products = body.get('products')  # Expecting a list of product dictionaries
#             status = "Pending"
#             created_at = datetime.now()

#             if not products:
#                 return JsonResponse({'error': 'Missing required product details'}, status=400)

#             # Insert or retrieve the order_id from placeorder
#             with connection.cursor() as cursor:
#                 # Check if an open order exists for the user in the placeorder table
#                 cursor.execute(""" 
#                     SELECT stockiest_order_id FROM placeorder 
#                     WHERE user_id = %s AND status = 'Pending'
#                 """, [user_id])
#                 placeorder = cursor.fetchone()

#                 if placeorder:
#                     # Use the existing stockiest_order_id (order_id)
#                     order_id = placeorder[0]
#                 else:
#                     # Create a new order in placeorder table
#                     cursor.execute(""" 
#                         INSERT INTO placeorder (user_id, user_role,created_date)
#                         VALUES (%s, %s, %s)
#                     """, [user_id, user_role, created_at])
#                     order_id = cursor.lastrowid

#                 # Insert each product into order_table_product
#                 for product in products:
#                     product_id = product.get('product_id')
#                     mrp = product.get('mrp')
#                     rate = product.get('rate')
#                     inv_qnty = product.get('inv_qnty')
#                     free_qnty = product.get('free_qnty')
#                     scheme_name = product.get('scheme_name')

#                     # Validate each product's required fields
#                     if not (product_id and mrp and rate and inv_qnty and free_qnty and scheme_name):
#                         return JsonResponse({'error': 'Missing required product details in one or more products'}, status=400)

#                     # Insert the product details into order_table_product
#                     cursor.execute(""" 
#                         INSERT INTO order_table_product (
#                             order_id, product_id, mrp,rate, quantity, free, scheme_name, 
#                             user_id, user_role, status, created_at
#                         )
#                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                     """, [
#                         order_id, product_id, mrp, rate, inv_qnty, free_qnty, scheme_name,
#                         user_id, user_role, status, created_at
#                     ])
#                     order_product_id = cursor.lastrowid  # This is the product's unique ID in the order_table_product

#             # Return a success response with order details
#             return JsonResponse({
#                 'message': 'Products added to cart successfully',
#                 'order_id': order_id,
#                 'order_product_id': [order_product_id for _ in products],  # List of product IDs added
#                 'user_id': user_id,
#                 'user_role': user_role
#             }, status=201)

#         except Exception as e:
#             # Log the error message for better debugging
#             return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)



from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime
import json

class AddToCart(View):
    @method_decorator(csrf_exempt)  # Disables CSRF for testing; remove in production if unnecessary
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_user_from_token(self, request):
        """
        Extracts user_id and user_role from the access token in the Authorization header.
        """
        auth = JWTAuthentication()
        try:
            # Extract token from Authorization header
            token = request.headers.get('Authorization', '').split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user_id = validated_token.get('customer_id')
            user_role = validated_token.get('role_name')

            if not user_id or not user_role:
                return None, None
            return user_id, user_role

        except (InvalidToken, TokenError, IndexError):
            return None, None

    def post(self, request, *args, **kwargs):
        try:
            # Get user_id and user_role from the JWT token
            user_id, user_role = self.get_user_from_token(request)
            if not user_id or not user_role:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Parse the incoming JSON payload
            body = json.loads(request.body)
            products = body.get('products')  # Expecting a list of product dictionaries
            status = "Pending"
            created_at = datetime.now()

            if not products:
                return JsonResponse({'error': 'Missing required product details'}, status=400)

            # Insert or retrieve the order_id from placeorder
            with connection.cursor() as cursor:
                # Check if an open order exists for the user in the placeorder table
                cursor.execute(""" 
                    SELECT stockiest_order_id FROM placeorder 
                    WHERE user_id = %s AND status = 'Pending'
                """, [user_id])
                placeorder = cursor.fetchone()

                if placeorder:
                    # Use the existing stockiest_order_id (order_id)
                    order_id = placeorder[0]
                else:
                    # Create a new order in placeorder table
                    cursor.execute(""" 
                        INSERT INTO placeorder (user_id, user_role, created_date)
                        VALUES (%s, %s, %s)
                    """, [user_id, user_role, created_at])
                    order_id = cursor.lastrowid

                # Initialize a list to store product IDs
                order_product_ids = []

                # Insert each product into order_table_product
                for product in products:
                    product_id = product.get('product_id')
                    mrp = product.get('mrp')
                    rate = product.get('rate')
                    inv_qnty = product.get('inv_qnty')
                    free_qnty = product.get('free_qnty')
                    scheme_name = product.get('scheme_name')

                    # Validate each product's required fields
                    if not (product_id and mrp and rate and inv_qnty and free_qnty and scheme_name):
                        return JsonResponse({'error': 'Missing required product details in one or more products'}, status=400)

                    # Insert the product details into order_table_product
                    cursor.execute(""" 
                        INSERT INTO order_table_product (
                            order_id, product_id, mrp, rate, quantity, free, scheme_name, 
                            user_id, user_role, status, created_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        order_id, product_id, mrp, rate, inv_qnty, free_qnty, scheme_name,
                        user_id, user_role, status, created_at
                    ])
                    # Collect the unique ID for each product
                    order_product_ids.append(cursor.lastrowid)

            # Return a success response with order details
            return JsonResponse({
                'message': 'Products added to cart successfully',
                'order_id': order_id,
                'order_product_id': order_product_ids,  # List of unique product IDs added
                'user_id': user_id,
                'user_role': user_role
            }, status=201)

        except Exception as e:
            # Log the error message for better debugging
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)









# from django.http import JsonResponse
# from django.views import View
# from django.db import connection
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# import json


# class CartDetailsView(View):
#     @method_decorator(csrf_exempt)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def get_user_from_token(self, request):
#         """
#         Extracts user_id and role_name from the access token in the Authorization header.
#         """
#         auth = JWTAuthentication()
#         try:
#             # Extract token from Authorization header
#             token = request.headers.get('Authorization', '').split(' ')[1]
#             validated_token = auth.get_validated_token(token)
#             user_id = validated_token.get('customer_id')
#             role_name = validated_token.get('role_name')
#             if not user_id or not role_name:
#                 return None, None
#             return user_id, role_name

#         except (InvalidToken, TokenError, IndexError):
#             return None, None

#     def post(self, request, *args, **kwargs):
#         """
#         Fetch cart details based on order_id and multiple order_product_ids.
#         """
#         try:
#             # Authenticate user
#             user_id, role_name = self.get_user_from_token(request)
#             if not user_id or not role_name:
#                 return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

#             # Parse the request body
#             body = json.loads(request.body)
#             order_id = body.get('order_id')
#             order_product_ids = body.get('order_product_id')

#             if not order_id or not order_product_ids:
#                 return JsonResponse({'error': 'order_id and order_product_id are required.'}, status=400)

#             # Ensure order_product_ids is a list
#             if isinstance(order_product_ids, list):
#                 order_product_ids = tuple(order_product_ids)  # Convert to tuple for SQL query
#             else:
#                 return JsonResponse({'error': 'order_product_id should be a list of IDs.'}, status=400)

#             # Query to fetch cart details for all order_product_ids
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT
#                         op.order_product_id,
#                         p.product_name,
#                         p.sku,
#                         op.quantity,
#                         op.free,
#                         op.scheme_name,
#                         (op.rate * op.quantity) AS total_amount
#                     FROM
#                         order_table_product op
#                     JOIN
#                         product p ON op.product_id = p.product_id
#                     WHERE
#                         op.order_id = %s AND op.order_product_id IN %s
#                 """, [order_id, order_product_ids])
#                 cart_details = cursor.fetchall()

#             if not cart_details:
#                 return JsonResponse({'error': 'No matching cart details found.'}, status=404)

#             # Calculate total amount and construct response
#             total_sum = 0
#             response_data = []
#             for cart_item in cart_details:
#                 total_sum += cart_item[6]  # Add the total_amount (index 6) to total_sum
#                 response_data.append({
#                     'order_product_id': cart_item[0],
#                     'product_name': cart_item[1],
#                     'sku': cart_item[2],
#                     'quantity': cart_item[3],
#                     'free': cart_item[4],
#                     'scheme_name': cart_item[5],
#                     'total_amount': cart_item[6],
#                 })

#             # Add the total sum at the end of the response
#             response_data.append({
#                 'total_amount_sum': total_sum
#             })

#             return JsonResponse({'cart_details': response_data}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)




class CartDetailsView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_user_from_token(self, request):
        """
        Extracts user_id and role_name from the access token in the Authorization header.
        """
        auth = JWTAuthentication()
        try:
            # Extract token from Authorization header
            token = request.headers.get('Authorization', '').split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user_id = validated_token.get('customer_id')
            role_name = validated_token.get('role_name')
            if not user_id or not role_name:
                return None, None
            return user_id, role_name

        except (InvalidToken, TokenError, IndexError):
            return None, None

    def post(self, request, *args, **kwargs):
        """
        Fetch cart details based on order_id.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Parse the request body
            body = json.loads(request.body)
            order_id = body.get('order_id')

            if not order_id:
                return JsonResponse({'error': 'order_id is required.'}, status=400)

            # Query to fetch cart details for all products in the given order_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        op.order_product_id,

                               
                        p.product_name,
                        p.sku,
                        op.quantity,
                        op.free,
                        op.scheme_name,
                        (op.rate * op.quantity) AS total_amount
                    FROM
                        order_table_product op
                    JOIN
                        product p ON op.product_id = p.product_id
                    WHERE
                        op.order_id = %s
                """, [order_id])
                cart_details = cursor.fetchall()

            if not cart_details:
                return JsonResponse({'error': 'No matching cart details found.'}, status=404)

            # Calculate total amount and construct response
            total_sum = 0
            response_data = []
            for cart_item in cart_details:
                total_sum += cart_item[6]  # Add the total_amount (index 6) to total_sum
                response_data.append({
                    'order_product_id': cart_item[0],
                    'product_name': cart_item[1],
                    'sku': cart_item[2],
                    'inv_qnty': cart_item[3],
                    'free_qnty': cart_item[4],
                    'scheme_name': cart_item[5],
                    'total_amount': round(cart_item[6],2)
                })

            # Add the total sum at the end of the response
            response_data.append({
                'total_amount_sum': round(total_sum,2)
            })

            return JsonResponse({'cart_details': response_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
