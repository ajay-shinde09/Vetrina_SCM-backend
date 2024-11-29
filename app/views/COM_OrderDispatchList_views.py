from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers.COM_OrderDispatchList_serializers import COMCustomerOrderListDispatchSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsCommercialOperationManager,IsNonAdminUser

class COMCustomerOrderListDispatchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationManager,IsNonAdminUser] 
    
    def get(self, request, *args, **kwargs):
        # SQL query to fetch the required data (without Sr.No in query)
        query = """
            SELECT 
                c.name AS customer_name,
                cr.role_name AS customer_role,
                po.created_date AS order_date,
                po.status AS order_status,
                ld.dispatch_date
            FROM 
                customer c
            JOIN 
                customer_roles cr ON c.role = cr.cust_role_id
            JOIN 
                placeorder po ON c.customer_id = po.user_id
			JOIN 
                lr_details ld ON po.stockiest_order_id = ld.order_id
            WHERE 
                po.status = 'Y'  -- Only Inprocess Orders
            ORDER BY 
                po.created_date
        """
        
        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Prepare response data with Sr.No calculated in Python
        data = []
        for idx, row in enumerate(rows):
            data.append({
                "sr_no": idx + 1,  # Sr.No is index + 1
                "customer_name": row[0],
                "customer_role": row[1],
                "order_date": row[2],
                "status": row[3],
                "dispatch_date": row[4]
            })

        # Serialize the data using the CustomerOrderSerializer
        serializer = COMCustomerOrderListDispatchSerializer(data=data, many=True)  # Passing data correctly
        
        # Return the serialized data as JSON
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)