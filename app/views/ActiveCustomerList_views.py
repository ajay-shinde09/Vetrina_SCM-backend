from django.urls import reverse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

from app.serializers.ActiveCustomerList_serializers import ActiveCustomerListSerializer

class ActiveCustomerListView(APIView):
    def get(self, request, *args, **kwargs):
        # SQL query to fetch the required data
        query = '''
        SELECT customer_id,
       name,
       owner_name,
       email,
       mobile_number,
       created_on
        FROM customer
        WHERE is_block = 'N'
        '''
        
        # Executing the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Preparing the response data
        response_data = []
        for row in rows:
            customer_id, name, owner_name, email, mobile_number, created_on = row
            response_data.append({
                "customer_id": customer_id,
                "name": name,
                "owner_name": owner_name,
                "email": email,
                "mobile_number": mobile_number,
                "created_on": created_on,
            })
        
        # Add Sr. No and Action link for each customer
        for indx, customer in enumerate(response_data, start=1):
            customer['sr_no'] = indx
            customer['actions'] = reverse('Active_customer_list_Detail', args=[customer['customer_id']])

        # Use serializer to structure the data
        serializer = ActiveCustomerListSerializer(response_data, many=True)

        # Return the serialized data
        return Response(serializer.data)
