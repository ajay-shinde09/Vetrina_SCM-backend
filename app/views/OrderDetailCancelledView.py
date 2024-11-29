from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.http import Http404

class OrderDetailCancelledView(APIView):
    def get(self, request, order_id, format=None):
        with connection.cursor() as cursor:
            # Query to join product, order_table_product, vetzone, and placeorder
            
            # Query to join product, customer_order_table_product, vetzone, and customer_placeorder
            cursor.execute('''
                SELECT 
                    p.product_name, 
                    p.sku, 
                    cop.quantity AS qty, 
                    cop.mrp, 
                    cop.rate, 
                    p.min_inventory_qnty AS miq,
                    cop.batch,  -- Added batch from customer_order_table_product
                    v.name AS customer_name,  -- Customer name from vetzone
                    po.payment_method,  -- Payment method from customer_placeorder
                    cop.product_id,  -- Added product_id for stock calculation
                    po.user_id  -- Added user_id for stock calculation (created_by)
                FROM 
                    customer_order_table_product cop
                JOIN 
                    customer_placeorder po ON cop.order_id = po.customer_order_id
                JOIN 
                    product p ON cop.product_id = p.product_id
                JOIN 
                    vetzone v ON po.user_id = v.vetzone_id
                WHERE 
                    po.customer_order_id = %s 
            ''', [order_id])
            
            result = cursor.fetchall()

            if not result:
                raise Http404("Order not found or not dispatched")

            # Extract customer_name and payment_method from the first result row
            customer_name = result[0][7] if len(result) > 0 else None
            payment_method = result[0][8] if len(result) > 0 else None

            # Prepare the response data
            data = {
                'customer_name': customer_name,  # Added customer name
                'order_id': order_id,
                'payment_mode': payment_method,  # Added payment method
                'products': []
            }

            sr_no = 1
            for row in result:
                if len(row) >= 10:
                    product_id = row[9]
                    created_by = row[10]
                    qty = row[2]

                    # Calculate stock for the product
                    cursor.execute('''
                        SELECT 
                            SUM(i.quantity) AS stock
                        FROM 
                            vetzone_instock AS i
                        INNER JOIN 
                            product AS p ON i.product_id = p.product_id
                        WHERE 
                            i.product_id = %s 
                            AND i.created_by = %s;
                    ''', [product_id, created_by])
                    
                    stock_result = cursor.fetchone()
                    stock = stock_result[0] if stock_result and stock_result[0] is not None else 0

                    # Calculate available quantity (stock - qty)
                    available_qty = stock - qty

                    # Calculate average quantity for the past 3 months (avgQty)
                    cursor.execute('''
                        SELECT 
                            SUM(quantity) / 3 AS avgQty
                        FROM 
                            customer_order_table_product
                        WHERE 
                            customer_id = %s 
                            AND created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                            AND product_id = %s;
                    ''', [created_by, product_id])

                    avg_qty_result = cursor.fetchone()
                    avg_qty = avg_qty_result[0] if avg_qty_result and avg_qty_result[0] is not None else 0

                    # Calculate min_inv_qty = (avgQty / 30) * 15
                    min_inv_qty = (avg_qty / 30) * 15 if avg_qty > 0 else 0

                    # Calculate average sale for the past 3 months (avgSale)
                    cursor.execute('''
                        SELECT 
                            SUM(cop.quantity * cop.rate) / 3 AS avgSale
                        FROM 
                            customer_order_table_product cop
                        WHERE 
                            cop.customer_id = %s
                            AND cop.created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
                            AND cop.product_id = %s;
                    ''', [created_by, product_id])

                    avg_sale_result = cursor.fetchone()
                    avg_sale = avg_sale_result[0] if avg_sale_result and avg_sale_result[0] is not None else 0

                    # Append the product details to the response
                    data['products'].append({
                        'sr_no': sr_no,
                        'product_name': row[0],
                        'sku': row[1],
                        'qty': qty,
                        'mrp': row[3],
                        'rate': row[4],
                        'sale': avg_sale,  # Added avgSale to the response
                        'available_qty': available_qty,
                        'miq': min_inv_qty,  # Updated miq with calculated value
                        'batch': row[6],  # Added batch to response
                        'act': None  # Act field, keeping it empty
                    })
                    sr_no += 1
                else:
                    # Debug: Print message if row has unexpected number of elements
                    print("Unexpected row length:", len(row))
        
        return Response(data)
