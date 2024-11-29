from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.VzOrdersCancelled_serializers import VzOrdersCancelledSerializer

class VzOrdersCancelledView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # Query to join vetzone and placeorder where status is 'P', with GROUP BY
            cursor.execute('''
                SELECT 
                    v.vetzone_id, 
                    v.name, 
                    p.created_date, 
                    p.status, 
                    p.stockiest_order_id 
                FROM 
                    order_table_product otp
                JOIN 
                    placeorder p ON otp.order_id = p.stockiest_order_id
                JOIN 
                    vetzone v ON p.user_id = v.vetzone_id
                WHERE 
                    p.status = 'N'
                GROUP BY 
                    v.vetzone_id, v.name, p.created_date, p.status, p.stockiest_order_id;
            ''')
            result = cursor.fetchall()

        # Prepare the response data
        data = []
        for idx, row in enumerate(result, start=1):
            vetzone_data = {
                'sr_no': idx,
                'vetzone_name': row[1],  # v.name
                'order_date': row[2],    # p.created_date
                'status': row[3],        # p.status
                'stockiest_order_id': row[4],  # p.stockiest_order_id (for action link)
            }
            serializer = VzOrdersCancelledSerializer(vetzone_data)
            data.append(serializer.data)

        return Response(data)
