import json
from django.db import connection
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers.PendingPlacedOrderDetails_serializers import PendingPlacedOrderDetailsSerializer
from decimal import Decimal
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsCommercialOperationManager,IsNonAdminUser
from django.db import connection, transaction
from django.utils import timezone

class PendingPlacedOrderDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationManager,IsNonAdminUser] 
    def get(self, request, order_id=None, batch=None):
        # Fetch customer details
        query_customer = """
            SELECT c.name AS customer_name, 
                   p.stockiest_order_id AS order_id, 
                   p.payment_method
            FROM customer c
            JOIN placeorder p ON c.customer_id = p.user_id
            WHERE p.stockiest_order_id = %s
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query_customer, [order_id])
            customer_data = cursor.fetchone()
        
        customer_info = {}
        if customer_data:
            customer_info = {
                "customer_name": customer_data[0],
                "order_id": customer_data[1],
                "payment_method": customer_data[2]
            }


        # Fetch order product details
        query_products = """
            SELECT 
                p.product_name AS Product,
                p.sku AS SKU,
                '' AS Batch,
                otp.quantity AS Qty,
                otp.free AS FreeQty,
                i.mrp AS MRP,
                i.pts AS Rate,
                '' AS Sale,
                '' AS AvailableQty,
                '' AS MIQ,
                '' AS Act,
                otp.product_id,
                otp.user_id,
                otp.user_role,
                otp.order_id,
                otp.scheme_name
            FROM 
                order_table_product otp
            INNER JOIN 
                product p ON otp.product_id = p.product_id
            INNER JOIN 
               (SELECT product_id, MAX(mrp) AS mrp, MAX(pts) AS pts FROM instock GROUP BY product_id) AS i ON i.product_id = p.product_id
            WHERE 
                otp.order_id = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query_products, [order_id])
            product_data = cursor.fetchall()

        columns = ["Product", "SKU", "Batch", "Qty", "FreeQty", "MRP", "Rate", "Sale", "AvailableQty", "MIQ", "Act", "product_id", "user_id","user_role","order_id","scheme_name"]

        data = []
        for idx, row in enumerate(product_data):
            row_data = dict(zip(columns, row))
            row_data["Sr"] = idx + 1

            # Extract user_id and product_id
            user_id = row_data["user_id"]
            product_id = row_data["product_id"]

            # Calculate Sale
            qty = Decimal(row_data["Qty"]) if row_data["Qty"] else Decimal(0)
            rate = Decimal(row_data["Rate"]) if row_data["Rate"] else Decimal(0)
            # qty = Decimal(row_data["Qty"])
            # rate = Decimal(row_data["Rate"])
            row_data["Sale"] = str(qty * rate)

            # Fetch avgQty over the last 3 months
            query_avg_qty = """
                SELECT SUM(quantity) / 3 AS avgQty
                FROM order_table_product
                WHERE user_id = %s
                  AND created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                  AND product_id = %s;
            """
            with connection.cursor() as cursor:
                cursor.execute(query_avg_qty, [user_id, product_id])
                avg_qty = cursor.fetchone()[0] or 0
                row_data["avgQty"] = avg_qty

            # Fetch stock quantity
            query_stock = """
                SELECT SUM(i.quantity) AS stock
                FROM instock AS i
                WHERE i.product_id = %s;
            """
            with connection.cursor() as cursor:
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
            with connection.cursor() as cursor:
                cursor.execute(query_total_qty, [user_id, product_id])
                row_data["totalQtyOrdered"] = cursor.fetchone()[0] or 0

            # Calculate AvailableQty and MIQ
            row_data["AvailableQty"] = str(float(stock) - float(row_data["totalQtyOrdered"]))
            row_data["MIQ"] = str((Decimal(avg_qty) / Decimal(30)) * Decimal(15))

            data.append(row_data)
           

        # Combine customer info and product details
        response_data = {
            "customer_info": customer_info,
            "products": data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, order_id, *args, **kwargs):
        action = request.data.get('action')
        comment = request.data.get('comment', '')
        products = request.data.get('products', [])

        if not action:
            return Response({"detail": "Missing required field: action."}, status=status.HTTP_400_BAD_REQUEST)
        if action == 'accept' and not products:
            return Response({"detail": "Missing required field: products."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                # Check if the order exists
                cursor.execute("""
                    SELECT stockiest_order_id 
                    FROM placeorder 
                    WHERE stockiest_order_id = %s
                """, [order_id])
                if not cursor.fetchone():
                    return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

                # Process 'accept' action
                if action == 'accept':
                    for product in products:
                        product_id = product.get('product_id')
                        batch = product.get('batch')
                        Qty = product.get('Qty')
                        FreeQty = product.get('FreeQty')
                        MRP = product.get('MRP')
                        Rate = product.get('Rate')

                        # Fetch an existing row for the product_id with an empty batch
                        cursor.execute("""
                            SELECT order_product_id 
                            FROM order_table_product 
                            WHERE order_id = %s AND product_id = %s AND (batch = '' OR batch IS NULL)
                            LIMIT 1
                        """, [order_id, product_id])
                        empty_batch_row = cursor.fetchone()

                        if empty_batch_row:
                            # Update the batch, quantity, free quantity, rate, and MRP for the existing empty row
                            cursor.execute("""
                                UPDATE order_table_product
                                SET batch = %s, quantity = %s, free = %s, mrp = %s, rate = %s
                                WHERE order_product_id = %s
                            """, [batch, Qty, FreeQty, MRP, Rate, empty_batch_row[0]])
                        else:
                            # Insert a new record for the product with the new batch and other fields
                            cursor.execute("""
                                INSERT INTO order_table_product (
                                    order_id, product_id, batch, rate, disc, tax, mrp, rate_mode, 
                                    quantity, free, scheme_name, user_id, user_role, status, created_at
                                )
                                SELECT %s, %s, %s, rate, disc, tax, %s, rate_mode, 
                                    %s, %s, scheme_name, user_id, user_role, 'Y', %s
                                FROM order_table_product
                                WHERE order_id = %s AND product_id = %s
                                LIMIT 1
                            """, [order_id, product_id, batch, MRP, Qty, FreeQty, timezone.now(), order_id, product_id])

                    # Update placeorder with comment and set status to 'I'
                    cursor.execute("""
                        UPDATE placeorder
                        SET comment = %s, status = 'I'
                        WHERE stockiest_order_id = %s
                    """, [comment, order_id])

                elif action == 'decline':
                    # Update placeorder status to 'N' and add comment
                    cursor.execute("""
                        UPDATE placeorder
                        SET comment = %s, status = 'N'
                        WHERE stockiest_order_id = %s
                    """, [comment, order_id])

                else:
                    return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"detail": "Order processed successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
    def delete(self, request, order_id):
        product_id = request.data.get('product_id')
        batch = request.data.get('batch')

        if not product_id:
            return Response(
                {"message": "product_id is required in the request body."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with connection.cursor() as cursor:
                # Delete the specific product for the given order
                cursor.execute(
                    """
                    DELETE FROM order_table_product
                    WHERE order_id = %s AND product_id = %s AND batch = %s
                    """,
                    [order_id, product_id, batch]
                )
                deleted_count = cursor.rowcount

                if deleted_count == 0:
                    return Response(
                        {"message": "No matching product found for the given order_id and product_id."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Check if there are any remaining products for the order
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM order_table_product
                    WHERE order_id = %s
                    """,
                    [order_id]
                )
                remaining_products = cursor.fetchone()[0]

                # If no products remain, update the status of the Placeorder entry
                if remaining_products == 0:
                    cursor.execute(
                        """
                        UPDATE placeorder
                        SET status = 'N'
                        WHERE stockiest_order_id = %s
                        """,
                        [order_id]
                    )

            return Response({"message": "Product deleted successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"message": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
