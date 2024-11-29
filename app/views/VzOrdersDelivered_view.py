from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.VzOrdersDelivered_serializers import VzOrdersDeliveredSerializer

class VzOrdersDeliveredView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # Query to fetch orders with status 'Dispatched'
            cursor.execute('''
                SELECT 
                    v.name,              -- Vetzone Name
                    p.created_date,      -- Order Date
                    p.status,            -- Status (should be 'Dispatched')
                    p.created_date as dispatch_date,     -- Dispatch Date
                    p.stockiest_order_id -- Order ID for Action URL
                FROM 
                    order_table_product otp
                JOIN 
                    placeorder p ON otp.order_id = p.stockiest_order_id
                JOIN 
                    vetzone v ON p.user_id = v.vetzone_id
                WHERE 
                    p.status = 'D' -- Change status to reflect dispatched orders
                GROUP BY 
                    p.stockiest_order_id, v.name, p.created_date, p.status;           
            ''')
            result = cursor.fetchall()

        # Prepare the response data
        data = []
        for idx, row in enumerate(result, start=1):
            vetzone_data = {
                'sr_no': idx,
                'vetzone_name': row[0],    # v.name
                'order_date': row[1],      # p.created_date
                'status': row[2],          # p.status
                'dispatch_date': row[3],   # p.dispatch_date (actual dispatch date)
                'stockiest_order_id': row[4]  # p.stockiest_order_id (for action link)
            }
            serializer = VzOrdersDeliveredSerializer(vetzone_data)
            data.append(serializer.data)

        return Response(data)
