import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.urls import reverse
from django.conf import settings 
from app.permissions import IsCnF, IsCustomer, IsStockiest,IsKeyAccount,IsRetailer,IsPetShop,IsFarmer,IsDoctor,IsLSS,IsPetOwner
from app.serializers.CreditPaymentOrders_Dispatched_serializers import CreditPaymentOrders_DispatchedResponseSerializer
# CreditPaymentOrders_Dispatchedserializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from urllib.parse import quote

class CreditPaymentOrders_DispatchedListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated|IsCustomer|IsCnF | IsStockiest|IsKeyAccount|IsRetailer|IsPetShop|IsFarmer|IsDoctor|IsLSS|IsPetOwner]

    def get(self, request):
        customer_id = request.GET.get('customer_id', None)

        if not customer_id:
            return Response(
                {"error": "customer_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with connection.cursor() as cursor:
            # Query for Customer Orders
            query = """
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
            cursor.execute(query, [customer_id])
            rows = cursor.fetchall()

            columns = [
                "OrderId", "customer_name", "customer_role",
                "order_date", "dispatch_date", "status",
                "file_path", "payment_method"
            ]

            data = []
            order_ids = []  # Collect Order IDs for the second query
            for index, row in enumerate(rows):
                customer = dict(zip(columns, row))
                customer['sr_no'] = index + 1
                customer['action'] = {
                    'link': reverse('COM_CustomerOrders_pending', args=[customer['OrderId']]),
                    'view_update_lr': 'view_update_File'
                }

                if customer['file_path']:
                    # Ensure the file path is URL-safe and uses forward slashes
                    sanitized_path = customer['file_path'].replace('\\', '/')  # Replace backslashes with forward slashes
                    encoded_path = quote(sanitized_path)  # Encode special characters like spaces
                    customer['file_url'] = f"{settings.MEDIA_URL}lr_files/{encoded_path}"
                else:
                    customer['file_url'] = None


                data.append(customer)
                order_ids.append(customer['OrderId'])  # Add OrderId for the next query

            # Query for Order Products
            product_data = []
            product_common = {}
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
                    INNER JOIN 
                        placeorder po ON otp.order_id = po.stockiest_order_id
                    LEFT JOIN 
                        invoice i ON po.stockiest_order_id = i.order_id
                    WHERE 
                        po.stockiest_order_id IN %s;
                """
                cursor.execute(product_query, [tuple(order_ids)])
                product_rows = cursor.fetchall()

                product_columns = [
                    "HSNNumber", "ProductName", "SKU", "Batch",
                    "Quantity", "MRP", "Rate"
                ]

                # Process Product Rows
                for indx, row in enumerate(product_rows):
                    product = dict(zip(product_columns, row))
                    product['SrNo'] = indx + 1
                    product_data.append(product)

                # Extract common fields from the first customer order
                if data:
                    first_order = data[0]
                    product_common = {
                        "CustomerName": first_order["customer_name"],
                        "OrderId": first_order["OrderId"],
                        "PaymentMode": first_order["payment_method"]
                    }
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

            # Add Total to each customer order
            for customer in data:
                customer['Total'] = invoice_totals.get(customer['OrderId'], 0)

        # Wrap `order_products` as a dictionary
        response_data = {
            "customer_orders": data,
            "order_products": {
                "common": product_common,
                "details": product_data  # List of product details without redundant fields
            },
           
        }

        serializer = CreditPaymentOrders_DispatchedResponseSerializer(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


        

    def put(self, request):
        new_lrno = request.data.get("lrno")

        if not new_lrno:
            return Response(
                {"error": "LR number is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the order_id from the GET request data (assuming the user will pass it)
        order_id = request.data.get("order_id")
        if not order_id:
            return Response(
                {"error": "Order ID is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify the existing lrno in the database for the specified order_id
        with connection.cursor() as cursor:
            cursor.execute("SELECT lrno FROM lr_details WHERE order_id = %s;", [order_id])
            result = cursor.fetchone()

            if result:
                existing_lrno = result[0]
                if existing_lrno != new_lrno:
                    return Response(
                        {"error": "LR number does not match the existing one."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Update the status in lr_details table
                cursor.execute(
                    "UPDATE lr_details SET is_verified = 'Y' WHERE order_id = %s;",
                    [order_id]
                )

                return Response({"message": "LR number verified and status updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Order ID not found."},
                    status=status.HTTP_404_NOT_FOUND
                )