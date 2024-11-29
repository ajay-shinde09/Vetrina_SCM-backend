# views.py
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse
from app.permissions import IsCommercialOperationManager, IsNonAdminUser
from app.serializers.ComCustomerOrders_pending_serializers import ComPendingCustomerOrderListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ComPendingCustomerOrderListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationManager,IsNonAdminUser]
    def get(self, request):
        query = '''
            SELECT 
    c.customer_id,
    c.name AS customer_name,
    cr.role_name AS customer_role,
    po.created_date AS order_date,
    po.status AS status,
    po.stockiest_order_id AS order_id
FROM 
    customer c
JOIN 
    customer_roles cr ON c.role = cr.cust_role_id
JOIN 
    placeorder po ON c.customer_id = po.user_id
WHERE 
    po.status = 'P' 
    AND cr.role_name != 'vetzone' -- Exclude vetzone
ORDER BY 
    po.created_date;

        '''
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Format data without sr_no and action_link initially
        data = [
            {
                'customer_id': row[0],
                'customer_name': row[1],
                'customer_role': row[2],
                'order_date': row[3],
                'status': row[4],
                'order_id': row[5]
            }
            for row in rows
        ]

        # Add sr_no and action_link
        # views.py
        for idx, customer in enumerate(data, start=1):
            customer['sr_no'] = idx  # Incremental serial number
            customer['action'] = reverse('COM_CustomerOrders_pending', args=[customer['order_id']]
            )
        # Serialize the data
        serializer = ComPendingCustomerOrderListSerializer(data, many=True)
        return Response(serializer.data)
