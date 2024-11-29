# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.db import connection
# from .VzOrdersPending_serializers import VzOrdersPendingSerializer

# class VzOrdersPendingView(APIView):
#     def get(self, request, *args, **kwargs):
#         with connection.cursor() as cursor:
#             # Query to join vetzone and placeorder where status is 'P', with GROUP BY
#             cursor.execute(''' 
#                 SELECT 
#                     v.vetzone_id, 
#                     v.name, 
#                     p.created_date, 
#                     p.status, 
#                     p.stockiest_order_id 
#                 FROM 
#                     order_table_product otp
#                 JOIN 
#                     placeorder p ON otp.order_id = p.stockiest_order_id
#                 JOIN 
#                     vetzone v ON p.user_id = v.vetzone_id
#                 WHERE 
#                     p.status = 'P'
#                 GROUP BY 
#                     v.vetzone_id, v.name, p.created_date, p.status, p.stockiest_order_id;
#             ''')
#             result = cursor.fetchall()

#         # Prepare the response data
#         data = []
#         for idx, row in enumerate(result, start=1):
#             vetzone_data = {
#                 'sr_no': idx,
#                 'vetzone_name': row[1],  # v.name
#                 'order_date': row[2],    # p.created_date
#                 'status': row[3],        # p.status
#                 'order_id': row[4],      # p.stockiest_order_id (rename for clarity)
#             }
#             serializer = VzOrdersPendingSerializer(vetzone_data)
#             data.append(serializer.data)

#         return Response(data)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.VzOrdersPending_serializers import VzOrdersPendingSerializer

class VzOrdersPendingView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            # Query to join customer_order_table_product and customer_placeorder where status is 'P', with GROUP BY
            cursor.execute(''' 
                SELECT 
                    v.vetzone_id, 
                    v.name, 
                    cp.created_date, 
                    cp.status, 
                    cp.customer_order_id 
                FROM 
                    customer_order_table_product cotp
                JOIN 
                    customer_placeorder cp ON cotp.order_id = cp.customer_order_id
                JOIN 
                    vetzone v ON cp.user_id = v.vetzone_id
                WHERE 
                    cp.status = 'P'
                GROUP BY 
                    v.vetzone_id, v.name, cp.created_date, cp.status, cp.customer_order_id;
            ''')
            result = cursor.fetchall()

        # Prepare the response data
        data = []
        for idx, row in enumerate(result, start=1):
            vetzone_data = {
                'sr_no': idx,
                'vetzone_name': row[1],  # v.name
                'order_date': row[2],    # cp.created_date
                'status': row[3],        # cp.status
                'order_id': row[4],      # cp.customer_order_id (rename for clarity)
            }
            serializer = VzOrdersPendingSerializer(vetzone_data)
            data.append(serializer.data)

        return Response(data)
