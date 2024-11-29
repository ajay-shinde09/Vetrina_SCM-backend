
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class VzQuantityandAmountView(APIView):
    def get(self, request):
        # Retrieve query parameters
        
        fromdate = request.query_params.get('fromdate')
        vetzone_id = request.query_params.get('vetzone')

        # Validate the action parameter

        # Validate the vetzone_id and fromdate parameters
        if not vetzone_id or not fromdate:
            return Response({"error": "vetzone and fromdate parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Execute the stock query using the vetzone_id and fromdate
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.product_name AS "Product Name", 
                    p.sku AS "SKU", 
                    COALESCE(stock_data.stock, 0) AS available_quantity,
                    stock_data.batch AS "Batch Number",
                    coalesce(c.rate * c.quantity, 0) as amount  -- Calculate amount as rate * quantity
                FROM 
                    product AS p
                LEFT JOIN 
                    (
                        SELECT 
                            product_id, 
                            batch,
                            SUM(quantity) AS stock
                        FROM 
                            vetzone_instock
                        WHERE 
                            created_by = %s  -- vetzone_id placeholder
                            AND DATE(created_on) = %s  -- date placeholder
                        GROUP BY 
                            product_id, batch
                    ) AS stock_data ON p.product_id = stock_data.product_id
                LEFT JOIN
                    customer_order_table_product AS c
                ON p.product_id = c.product_id
                WHERE 
                    stock_data.product_id IS NOT NULL;
            """
            cursor.execute(query, [vetzone_id, fromdate])
            result = cursor.fetchall()

        # Step 2: Prepare response data with SR.No., available quantity, and amount
        response_data = [
            {
                "SR.No.": index + 1,  # Adding serial number starting from 1
                "product_name": row[0],
                "sku": row[1],
                "batch_number": row[3],
                "available_quantity": row[2],
                "amount": row[4],  # Include the calculated amount
            }
            for index, row in enumerate(result)  # Using enumerate to get index
        ]

        return Response(response_data)
