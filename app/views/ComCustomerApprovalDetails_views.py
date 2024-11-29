from decimal import Decimal
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers.ComCustomerApprovalDetails_serializers import ComBatchAllocatedDetailsSerializer
from rest_framework import status
from collections import namedtuple
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsCommercialOperationManager,IsNonAdminUser

class ComBatchAllocatedDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationManager,IsNonAdminUser] 
    def get(self, request, order_id=None):
        # Fetch customer details
        query_customer = """
            SELECT c.name AS customer_name, 
                   p.stockiest_order_id AS order_id, 
                   p.payment_method
            FROM customer c
            JOIN placeorder p ON c.customer_id = p.user_id
            WHERE p.stockiest_order_id = %s
        """

        # Fetch product details
        query_products = """
            SELECT 
                p.product_name AS Product,
                p.sku AS SKU,
                otp.batch AS Batch,
                otp.quantity AS Qty,
                otp.free AS FreeQty,
                i.mrp AS MRP,
                i.pts AS Rate,
                '' AS Sale,
                '' AS AvailableQty,
                '' AS MIQ,
                '' AS Act,
                otp.product_id,
                otp.user_id
            FROM 
                order_table_product otp
            INNER JOIN 
                product p ON otp.product_id = p.product_id
            INNER JOIN 
               (SELECT product_id, MAX(mrp) AS mrp, MAX(pts) AS pts FROM instock GROUP BY product_id) AS i ON i.product_id = p.product_id
            WHERE 
                otp.order_id = %s
        """

        response_data = {}

        with connection.cursor() as cursor:
            # Execute the first query for customer details
            cursor.execute(query_customer, [order_id])
            row = cursor.fetchone()

            if not row:
                return Response(
                    {"detail": "No customer details found for the given order ID."},
                    status=status.HTTP_404_NOT_FOUND
                )

            CustomerData = namedtuple('CustomerData', ['customer_name', 'order_id', 'payment_method'])
            customer_data = CustomerData._make(row)._asdict()
            response_data['customer_details'] = customer_data

            # Execute the second query for product details
            cursor.execute(query_products, [order_id])
            rows = cursor.fetchall()

            ProductData = namedtuple('ProductData', [
                'Product', 'SKU', 'Batch', 'Qty', 'FreeQty', 'MRP', 'Rate', 
                'Sale', 'AvailableQty', 'MIQ', 'Act', 'product_id', 'user_id'
            ])

            product_data = []
            for idx, row in enumerate(rows):
                row_data = ProductData._make(row)._asdict()
                row_data["SrNo"] = idx + 1

                # Extract user_id and product_id
                user_id = row_data["user_id"]
                product_id = row_data["product_id"]

                # Calculate Sale
                qty = Decimal(row_data["Qty"]) if row_data["Qty"] else Decimal(0)
                rate = Decimal(row_data["Rate"]) if row_data["Rate"] else Decimal(0)
                row_data["Sale"] = str(qty * rate)

                # Fetch avgQty over the last 3 months
                query_avg_qty = """
                    SELECT SUM(quantity) / 3 AS avgQty
                    FROM order_table_product
                    WHERE user_id = %s
                      AND created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                      AND product_id = %s;
                """
                cursor.execute(query_avg_qty, [user_id, product_id])
                avg_qty = cursor.fetchone()[0] or 0
                row_data["avgQty"] = avg_qty

                # Fetch stock quantity
                query_stock = """
                    SELECT SUM(i.quantity) AS stock
                    FROM instock AS i
                    WHERE i.product_id = %s;
                """
                cursor.execute(query_stock, [product_id])
                stock = cursor.fetchone()[0] or 0
                row_data["stock"] = stock

                # Fetch total ordered quantity by user
                query_total_qty = """
                    SELECT SUM(quantity) AS qty
                    FROM order_table_product
                    WHERE user_id = %s
                      AND product_id = %s;
                """
                cursor.execute(query_total_qty, [user_id, product_id])
                total_qty_ordered = cursor.fetchone()[0] or 0
                row_data["totalQtyOrdered"] = total_qty_ordered

                # Calculate AvailableQty and MIQ
                row_data["AvailableQty"] = str(float(stock) - float(total_qty_ordered))
                row_data["MIQ"] = str((Decimal(avg_qty) / Decimal(30)) * Decimal(15))

                product_data.append(row_data)

            response_data['product_details'] = product_data

        serializer = ComBatchAllocatedDetailsSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
