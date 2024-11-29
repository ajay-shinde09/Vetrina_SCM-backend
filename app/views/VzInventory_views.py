from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework import status

class VetZoneProductAvailabilityView(APIView):
    def get(self, request, vetzone_id):
        try:
            # Query to fetch the product data along with available quantity
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT 
                        p.product_name, 
                        p.sku, 
                        p.product_code, 
                        COALESCE(stock_data.stock, 0) - COALESCE(order_data.ordered_qty, 0) AS available_qty
                    FROM 
                        product AS p
                    LEFT JOIN 
                        (
                            SELECT 
                                product_id, 
                                SUM(quantity) AS stock
                            FROM 
                                vetzone_instock
                            WHERE 
                                created_by = %s
                            GROUP BY 
                                product_id
                        ) AS stock_data ON p.product_id = stock_data.product_id
                    LEFT JOIN 
                        (
                            SELECT 
                                product_id, 
                                SUM(quantity) AS ordered_qty
                            FROM 
                                customer_order_table_product
                            WHERE 
                                seller_user_id = %s 
                                AND seller_user_role = 'VetZone'
                            GROUP BY 
                                product_id
                        ) AS order_data ON p.product_id = order_data.product_id
                    WHERE 
                        stock_data.product_id IS NOT NULL OR order_data.product_id IS NOT NULL;
                ''', [vetzone_id, vetzone_id])
                
                product_rows = cursor.fetchall()
                
                # If no products found, return 404
                if not product_rows:
                    return Response({"error": "No products found for the given VetZone."}, status=status.HTTP_404_NOT_FOUND)
                
                # Prepare the product data for response
                products_data = []
                for row in product_rows:
                    product_name, sku, product_code, available_qty = row
                    products_data.append({
                        "Product Name": product_name,
                        "SKU": sku,
                        "Product Code": product_code,
                        "Available Quantity": available_qty
                    })
            
            # Return the product data
            return Response(products_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)