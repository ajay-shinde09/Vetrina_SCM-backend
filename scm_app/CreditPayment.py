# from django.db import connection
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.urls import reverse
# from django.conf import settings
# from urllib.parse import quote


# class CreditPaymentOrders_DispatchedListView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Retrieve the customer_id from the request query params
#         customer_id = request.GET.get('customer_id')

#         if not customer_id:
#             return Response(
#                 {"error": "customer_id is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with connection.cursor() as cursor:
#             # Fetch customer orders
#             order_query = """
#                 SELECT 
#                     p.stockiest_order_id AS OrderId,
#                     c.name AS customer_name,
#                     cr.role_name AS customer_role,
#                     p.created_date AS order_date,
#                     p.created_date AS dispatch_date,
#                     p.status AS status,
#                     lr.file AS file_path,
#                     p.payment_method AS payment_method
#                 FROM 
#                     placeorder p
#                 JOIN 
#                     customer c ON p.user_id = c.customer_id
#                 JOIN 
#                     customer_roles cr ON c.role = cr.cust_role_id
#                 LEFT JOIN 
#                     lr_details lr ON p.stockiest_order_id = lr.order_id
#                 WHERE 
#                     p.status = 'Y' AND c.customer_id = %s;
#             """
#             cursor.execute(order_query, [customer_id])
#             orders = cursor.fetchall()

#             order_columns = [
#                 "OrderId", "customer_name", "customer_role",
#                 "order_date", "dispatch_date", "status",
#                 "file_path", "payment_method"
#             ]
#             order_data = []
#             order_ids = []

#             # Process orders
#             for index, row in enumerate(orders):
#                 order = dict(zip(order_columns, row))
#                 order['sr_no'] = index + 1
#                 order['action'] = {
#                     'link': reverse('COM_CustomerOrders_pending', args=[order['OrderId']]),
#                     'view_update_lr': 'view_update_File'
#                 }
#                 # Handle file path sanitization
#                 if order['file_path']:
#                     sanitized_path = order['file_path'].replace('\\', '/')
#                     encoded_path = quote(sanitized_path)
#                     order['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
#                 else:
#                     order['file_url'] = None

#                 order_data.append(order)
#                 order_ids.append(order['OrderId'])

#             # Fetch products linked to the orders
#             product_data = []
#             if order_ids:
#                 product_query = """
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
#                         otp.order_id IN %s;
#                 """
#                 cursor.execute(product_query, [tuple(order_ids)])
#                 product_rows = cursor.fetchall()

#                 product_columns = [
#                     "HSNNumber", "ProductName", "SKU", "Batch",
#                     "Quantity", "MRP", "Rate"
#                 ]
#                 for row in product_rows:
#                     product = dict(zip(product_columns, row))
#                     product_data.append(product)

#             # Fetch invoice totals
#             invoice_totals = {}
#             if order_ids:
#                 invoice_query = """
#                     SELECT 
#                         order_id, SUM(invoice_amount) AS Total
#                     FROM 
#                         invoice
#                     WHERE 
#                         order_id IN %s
#                     GROUP BY 
#                         order_id;
#                 """
#                 cursor.execute(invoice_query, [tuple(order_ids)])
#                 invoice_rows = cursor.fetchall()
#                 invoice_totals = {row[0]: row[1] for row in invoice_rows}

#             # Append totals to orders
#             for order in order_data:
#                 order['Total'] = invoice_totals.get(order['OrderId'], 0)

#         # Construct the response data
#         response_data = {
#             "customer_orders": order_data,
#             "order_products": product_data,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)

#     def put(self, request):
#         # Update LR number
#         order_id = request.data.get("order_id")
#         new_lrno = request.data.get("lrno")

#         if not order_id or not new_lrno:
#             return Response(
#                 {"error": "Order ID and LR number are required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         with connection.cursor() as cursor:
#             cursor.execute("SELECT lrno FROM lr_details WHERE order_id = %s;", [order_id])
#             existing = cursor.fetchone()

#             if not existing:
#                 return Response(
#                     {"error": "Order ID not found."},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             if existing[0] != new_lrno:
#                 return Response(
#                     {"error": "LR number does not match the existing record."},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             cursor.execute(
#                 "UPDATE lr_details SET is_verified = 'Y' WHERE order_id = %s;",
#                 [order_id]
#             )

#         return Response({"message": "LR number verified successfully."}, status=status.HTTP_200_OK)


from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from urllib.parse import quote
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

# Custom method to extract and validate JWT token
def get_user_from_token(request):
    """
    Extracts user_id and role_name from the access token in the Authorization header.
    """
    auth = JWTAuthentication()
    try:
        token = request.headers.get('Authorization', '').split(' ')[1]
        validated_token = auth.get_validated_token(token)
        user_id = validated_token.get('customer_id')
        role_name = validated_token.get('role_name')
        if not user_id or not role_name:
            return None, None
        return user_id, role_name
    except (InvalidToken, TokenError, IndexError):
        return None, None


class CreditPaymentOrders_DispatchedListView(APIView):
    """
    API view for handling dispatched customer orders and their details.
    """

    def get(self, request):
        """
        Retrieve a list of dispatched customer orders along with their product and invoice details.
        """
        # Authenticate user and extract customer_id
        customer_id = get_user_from_token(request)
        if not customer_id:
            return Response(
                {"error": "Authentication failed. Invalid or missing token."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        with connection.cursor() as cursor:
            # Query to fetch orders based on customer ID
            order_query = """
                SELECT 
                    p.stockiest_order_id AS OrderId,
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
                    p.status = 'Y' AND c.customer_id = %s;
            """
            cursor.execute(order_query, [customer_id])
            orders = cursor.fetchall()

            # Define column mappings for orders
            order_columns = [
                "OrderId", "customer_name", "customer_role",
                "order_date", "dispatch_date", "status",
                "file_path", "payment_method"
            ]
            order_data = []
            order_ids = []

            # Process each order record
            for index, row in enumerate(orders):
                order = dict(zip(order_columns, row))
                order['sr_no'] = index + 1
                order['action'] = {
                    'link': reverse('COM_CustomerOrders_pending', args=[order['OrderId']]),
                    'view_update_lr': 'view_update_File'
                }
                # Handle file path sanitization
                if order['file_path']:
                    sanitized_path = order['file_path'].replace('\\', '/')
                    encoded_path = quote(sanitized_path)
                    order['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
                else:
                    order['file_url'] = None

                order_data.append(order)
                order_ids.append(order['OrderId'])

            # Fetch products linked to the orders
            product_data = []
            if order_ids:
                product_query = """
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
                        otp.order_id IN %s;
                """
                cursor.execute(product_query, [tuple(order_ids)])
                product_rows = cursor.fetchall()

                product_columns = [
                    "HSNNumber", "ProductName", "SKU", "Batch",
                    "Quantity", "MRP", "Rate"
                ]
                for row in product_rows:
                    product = dict(zip(product_columns, row))
                    product_data.append(product)

            # Fetch invoice totals
            invoice_totals = {}
            if order_ids:
                invoice_query = """
                    SELECT 
                        order_id, SUM(invoice_amount) AS Total
                    FROM 
                        invoice
                    WHERE 
                        order_id IN %s
                    GROUP BY 
                        order_id;
                """
                cursor.execute(invoice_query, [tuple(order_ids)])
                invoice_rows = cursor.fetchall()
                invoice_totals = {row[0]: row[1] for row in invoice_rows}

            # Append totals to each order
            for order in order_data:
                order['Total'] = invoice_totals.get(order['OrderId'], 0)

        # Construct the response
        response_data = {
            "customer_orders": order_data,
            "order_products": product_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
