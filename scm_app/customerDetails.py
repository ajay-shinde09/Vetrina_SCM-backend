# from django.http import JsonResponse
# from django.views import View
# from django.db import connection
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from urllib.parse import quote
# from django.conf import settings
# from django.urls import reverse
# from rest_framework.response import Response
# from rest_framework import status

# class CustomerDetails(View):
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

#     def get(self, request, *args, **kwargs):
#         """
#         Fetch cart details based on order_id and lrno (order_product_id) from GET parameters.
#         """
#         try:
#             # Authenticate user
#             user_id, role_name = self.get_user_from_token(request)
#             if not user_id or not role_name:
#                 return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

#             # Get parameters from the query string (URL parameters)
#             order_id = request.GET.get('order_id')
#             lrno = request.GET.get('lrno')

#             if not order_id or not lrno:
#                 return JsonResponse({'error': 'order_id and lrno are required.'}, status=400)

#             # Query to fetch order and customer details based on the order_id
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         p.stockiest_order_id AS OrderId,
#                         c.name AS customer_name,
#                         cr.role_name AS customer_role,
#                         p.created_date AS order_date,
#                         p.created_date AS dispatch_date,
#                         p.status AS status,
#                         lr.file AS file_path,
#                         p.payment_method AS payment_method
#                     FROM 
#                         placeorder p
#                     JOIN 
#                         customer c ON p.user_id = c.customer_id
#                     JOIN 
#                         customer_roles cr ON c.role = cr.cust_role_id
#                     LEFT JOIN 
#                         lr_details lr ON p.stockiest_order_id = lr.order_id
#                     WHERE 
#                         p.status = 'Y' AND p.stockiest_order_id = %s;
#                 """, [order_id])
#                 order_details = cursor.fetchone()

#                 if not order_details:
#                     return JsonResponse({'error': 'Order not found.'}, status=404)

#                 # Define column mappings for order details
#                 order_columns = [
#                     "OrderId", "customer_name", "customer_role", "order_date",
#                     "dispatch_date", "status", "file_path", "payment_method"
#                 ]
#                 order_data = dict(zip(order_columns, order_details))

#                 # Handle file path sanitization
#                 if order_data['file_path']:
#                     sanitized_path = order_data['file_path'].replace('\\', '/')
#                     encoded_path = quote(sanitized_path)
#                     order_data['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
#                 else:
#                     order_data['file_url'] = None

#                 # Fetch products linked to the order
#                 cursor.execute("""
#                     SELECT 
#                         p.hsn_code AS HSNNumber,
#                         p.product_name AS ProductName,
#                         p.sku AS SKU,
#                         otp.batch AS Batch,
#                         otp.quantity AS Quantity,
#                         otp.mrp AS MRP,
#                         otp.rate AS Rate
#                     FROM 
#                         order_table_product otp
#                     INNER JOIN 
#                         product p ON otp.product_id = p.product_id
#                     WHERE 
#                         otp.order_id = %s;
#                 """, [order_id])
#                 product_rows = cursor.fetchall()

#                 product_columns = ["HSNNumber", "ProductName", "SKU", "Batch", "Quantity", "MRP", "Rate"]
#                 product_data = [dict(zip(product_columns, row)) for row in product_rows]

#                 # Fetch invoice totals for the order
#                 cursor.execute("""
#                     SELECT 
#                         SUM(invoice_amount) AS Total
#                     FROM 
#                         invoice
#                     WHERE 
#                         order_id = %s
#                 """, [order_id])
#                 invoice_row = cursor.fetchone()
#                 invoice_total = invoice_row[0] if invoice_row else 0

#                 # Append the total invoice amount to the order data
#                 order_data['Total'] = invoice_total

#             # Construct the response with all the data
#             response_data = {
#                 "order_details": order_data,
#                 "order_products": product_data
#             }

#             return JsonResponse(response_data, status=200)

#         except Exception as e:
#             return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)



from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import quote
from django.conf import settings

class DispatchCustomerDetails(View):
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

    def get(self, request, *args, **kwargs):
        """
        Fetch order details based on order_id from GET parameters.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Get order_id from the query string (URL parameters)
            order_id = request.GET.get('order_id')

            if not order_id:
                return JsonResponse({'error': 'order_id is required.'}, status=400)

            # Query to fetch order and customer details based on the order_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.stockiest_order_id AS order_id,
                        c.name AS customer_name,
                        cr.role_name AS customer_role,
                        p.created_date AS order_date,
                        p.created_date AS dispatch_date,
                        p.status AS status,
                        lr.file AS file_path,
                        p.payment_method AS payment_method
                    FROM 
                        placeorder p
                    JOIN 
                        customer c ON p.user_id = c.customer_id
                    JOIN 
                        customer_roles cr ON c.role = cr.cust_role_id
                    LEFT JOIN 
                        lr_details lr ON p.stockiest_order_id = lr.order_id
                    WHERE 
                        p.status = 'Y' AND p.stockiest_order_id = %s;
                """, [order_id])
                order_details = cursor.fetchone()

                if not order_details:
                    return JsonResponse({'error': 'Order not found.'}, status=404)

                # Define column mappings for order details
                order_columns = [
                    "order_id", "customer_name", "user_role", "order_date",
                    "dispatch_date", "status", "file_path", "payment_method"
                ]
                order_data = dict(zip(order_columns, order_details))

                # Handle file path sanitization
                if order_data['file_path']:
                    sanitized_path = order_data['file_path'].replace('\\', '/')
                    encoded_path = quote(sanitized_path)
                    order_data['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
                else:
                    order_data['file_url'] = None

                # Fetch products linked to the order
                cursor.execute("""
                    SELECT 
                        p.hsn_code AS HSNNumber,
                        p.product_name AS ProductName,
                        p.sku AS SKU,
                        otp.batch AS Batch,
                        otp.quantity AS Quantity,
                        otp.mrp AS MRP,
                        otp.rate AS Rate
                    FROM 
                        order_table_product otp
                    INNER JOIN 
                        product p ON otp.product_id = p.product_id
                    WHERE 
                        otp.order_id = %s;
                """, [order_id])
                product_rows = cursor.fetchall()

                product_columns = ["HSNNumber", "product_name", "sku", "batch", "quantity", "mrp", "rate"]
                product_data = [dict(zip(product_columns, row)) for row in product_rows]

                # Fetch invoice totals for the order
                cursor.execute("""
                    SELECT 
                        SUM(invoice_amount) AS Total
                    FROM 
                        invoice
                    WHERE 
                        order_id = %s
                """, [order_id])
                invoice_row = cursor.fetchone()
                invoice_total = invoice_row[0] if invoice_row else 0

                # Append the total invoice amount to the order data
                order_data['Total'] = invoice_total

            # Construct the response with all the data
            response_data = {
                "order_details": order_data,
                "order_products": product_data
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)



class InprocessCustomerDetails(View):
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

    def get(self, request, *args, **kwargs):
        """
        Fetch order details based on order_id from GET parameters.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Get order_id from the query string (URL parameters)
            order_id = request.GET.get('order_id')

            if not order_id:
                return JsonResponse({'error': 'order_id is required.'}, status=400)

            # Query to fetch order and customer details based on the order_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.stockiest_order_id AS order_id,
                        c.name AS customer_name,
                        cr.role_name AS customer_role,
                        p.created_date AS order_date,
                        p.created_date AS dispatch_date,
                        p.status AS status,
                        lr.file AS file_path,
                        p.payment_method AS payment_method
                    FROM 
                        placeorder p
                    JOIN 
                        customer c ON p.user_id = c.customer_id
                    JOIN 
                        customer_roles cr ON c.role = cr.cust_role_id
                    LEFT JOIN 
                        lr_details lr ON p.stockiest_order_id = lr.order_id
                    WHERE 
                        p.status = 'I' AND p.stockiest_order_id = %s;
                """, [order_id])
                order_details = cursor.fetchone()

                if not order_details:
                    return JsonResponse({'error': 'Order not found.'}, status=404)

                # Define column mappings for order details
                order_columns = [
                    "order_id", "customer_name", "user_role", "order_date",
                    "dispatch_date", "status", "file_path", "payment_method"
                ]
                order_data = dict(zip(order_columns, order_details))

                # Handle file path sanitization
                if order_data['file_path']:
                    sanitized_path = order_data['file_path'].replace('\\', '/')
                    encoded_path = quote(sanitized_path)
                    order_data['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
                else:
                    order_data['file_url'] = None

                # Fetch products linked to the order
                cursor.execute("""
                    SELECT 
                        p.hsn_code AS HSNNumber,
                        p.product_name AS ProductName,
                        p.sku AS SKU,
                        otp.batch AS Batch,
                        otp.quantity AS Quantity,
                        otp.mrp AS MRP,
                        otp.rate AS Rate
                    FROM 
                        order_table_product otp
                    INNER JOIN 
                        product p ON otp.product_id = p.product_id
                    WHERE 
                        otp.order_id = %s;
                """, [order_id])
                product_rows = cursor.fetchall()

                product_columns = ["HSNNumber", "product_name", "sku", "batch", "quantity", "mrp", "rate"]
                product_data = [dict(zip(product_columns, row)) for row in product_rows]

                # Fetch invoice totals for the order
                cursor.execute("""
                    SELECT 
                        SUM(invoice_amount) AS Total
                    FROM 
                        invoice
                    WHERE 
                        order_id = %s
                """, [order_id])
                invoice_row = cursor.fetchone()
                invoice_total = invoice_row[0] if invoice_row else 0

                # Append the total invoice amount to the order data
                order_data['Total'] = invoice_total

            # Construct the response with all the data
            response_data = {
                "order_details": order_data,
                "order_products": product_data
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)


class DeliveredCustomerDetails(View):
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

    def get(self, request, *args, **kwargs):
        """
        Fetch order details based on order_id from GET parameters.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Get order_id from the query string (URL parameters)
            order_id = request.GET.get('order_id')

            if not order_id:
                return JsonResponse({'error': 'order_id is required.'}, status=400)

            # Query to fetch order and customer details based on the order_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.stockiest_order_id AS order_id,
                        c.name AS customer_name,
                        cr.role_name AS customer_role,
                        p.created_date AS order_date,
                        p.created_date AS dispatch_date,
                        p.status AS status,
                        lr.file AS file_path,
                        p.payment_method AS payment_method
                    FROM 
                        placeorder p
                    JOIN 
                        customer c ON p.user_id = c.customer_id
                    JOIN 
                        customer_roles cr ON c.role = cr.cust_role_id
                    LEFT JOIN 
                        lr_details lr ON p.stockiest_order_id = lr.order_id
                    WHERE 
                        p.status = 'D' AND p.stockiest_order_id = %s;
                """, [order_id])
                order_details = cursor.fetchone()

                if not order_details:
                    return JsonResponse({'error': 'Order not found.'}, status=404)

                # Define column mappings for order details
                order_columns = [
                    "order_id", "customer_name", "user_role", "order_date",
                    "dispatch_date", "status", "file_path", "payment_method"
                ]
                order_data = dict(zip(order_columns, order_details))

                # Handle file path sanitization
                if order_data['file_path']:
                    sanitized_path = order_data['file_path'].replace('\\', '/')
                    encoded_path = quote(sanitized_path)
                    order_data['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
                else:
                    order_data['file_url'] = None

                # Fetch products linked to the order
                cursor.execute("""
                    SELECT 
                        p.hsn_code AS HSNNumber,
                        p.product_name AS ProductName,
                        p.sku AS SKU,
                        otp.batch AS Batch,
                        otp.quantity AS Quantity,
                        otp.mrp AS MRP,
                        otp.rate AS Rate
                    FROM 
                        order_table_product otp
                    INNER JOIN 
                        product p ON otp.product_id = p.product_id
                    WHERE 
                        otp.order_id = %s;
                """, [order_id])
                product_rows = cursor.fetchall()

                product_columns = ["HSNNumber", "product_name", "sku", "batch", "quantity", "mrp", "rate"]
                product_data = [dict(zip(product_columns, row)) for row in product_rows]

                # Fetch invoice totals for the order
                cursor.execute("""
                    SELECT 
                        SUM(invoice_amount) AS Total
                    FROM 
                        invoice
                    WHERE 
                        order_id = %s
                """, [order_id])
                invoice_row = cursor.fetchone()
                invoice_total = invoice_row[0] if invoice_row else 0

                # Append the total invoice amount to the order data
                order_data['Total'] = invoice_total

            # Construct the response with all the data
            response_data = {
                "order_details": order_data,
                "order_products": product_data
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
        

class PendingCustomerDetails(View):
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

    def get(self, request, *args, **kwargs):
        """
        Fetch order details based on order_id from GET parameters.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Get order_id from the query string (URL parameters)
            order_id = request.GET.get('order_id')

            if not order_id:
                return JsonResponse({'error': 'order_id is required.'}, status=400)

            # Query to fetch order and customer details based on the order_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.stockiest_order_id AS order_id,
                        c.name AS customer_name,
                        cr.role_name AS customer_role,
                        p.created_date AS order_date,
                        p.created_date AS dispatch_date,
                        p.status AS status,
                        lr.file AS file_path,
                        p.payment_method AS payment_method
                    FROM 
                        placeorder p
                    JOIN 
                        customer c ON p.user_id = c.customer_id
                    JOIN 
                        customer_roles cr ON c.role = cr.cust_role_id
                    LEFT JOIN 
                        lr_details lr ON p.stockiest_order_id = lr.order_id
                    WHERE 
                        p.status = 'P' AND p.stockiest_order_id = %s;
                """, [order_id])
                order_details = cursor.fetchone()

                if not order_details:
                    return JsonResponse({'error': 'Order not found.'}, status=404)

                # Define column mappings for order details
                order_columns = [
                    "order_id", "customer_name", "user_role", "order_date",
                    "dispatch_date", "status", "file_path", "payment_method"
                ]
                order_data = dict(zip(order_columns, order_details))

                # Handle file path sanitization
                if order_data['file_path']:
                    sanitized_path = order_data['file_path'].replace('\\', '/')
                    encoded_path = quote(sanitized_path)
                    order_data['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
                else:
                    order_data['file_url'] = None

                # Fetch products linked to the order
                cursor.execute("""
                    SELECT 
                        p.hsn_code AS HSNNumber,
                        p.product_name AS ProductName,
                        p.sku AS SKU,
                        otp.batch AS Batch,
                        otp.quantity AS Quantity,
                        otp.mrp AS MRP,
                        otp.rate AS Rate
                    FROM 
                        order_table_product otp
                    INNER JOIN 
                        product p ON otp.product_id = p.product_id
                    WHERE 
                        otp.order_id = %s;
                """, [order_id])
                product_rows = cursor.fetchall()

                product_columns = ["HSNNumber", "product_name", "sku", "batch", "quantity", "mrp", "rate"]
                product_data = [dict(zip(product_columns, row)) for row in product_rows]

                # Fetch invoice totals for the order
                cursor.execute("""
                    SELECT 
                        SUM(invoice_amount) AS Total
                    FROM 
                        invoice
                    WHERE 
                        order_id = %s
                """, [order_id])
                invoice_row = cursor.fetchone()
                invoice_total = invoice_row[0] if invoice_row else 0

                # Append the total invoice amount to the order data
                order_data['Total'] = invoice_total

            # Construct the response with all the data
            response_data = {
                "order_details": order_data,
                "order_products": product_data
            }

            return JsonResponse(response_data, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

