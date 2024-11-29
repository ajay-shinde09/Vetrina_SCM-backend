from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.CandF_Dropdown_serializers import CandFDropdownSerializer

class CandFDropdownView(APIView):
    def get(self, request, *args, **kwargs):
        query = """
        SELECT customer_id, name 
        FROM customer 
        WHERE role = 1;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        # Transform the result into a list of dictionaries
        customers_data = [{'customer_id': row[0], 'name': row[1]} for row in result]

        # Pass the data directly to the serializer for serialization
        serializer = CandFDropdownSerializer(customers_data, many=True)
        return Response(serializer.data)
