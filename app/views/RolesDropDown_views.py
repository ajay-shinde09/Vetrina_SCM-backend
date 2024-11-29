from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.RolesDropDown_serializers import CustomerRoleSerializer

class CustomerRoleDropdownView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT cust_role_id, role_name FROM customer_roles")
            rows = cursor.fetchall()

        roles = [{'cust_role_id': row[0], 'role_name': row[1]} for row in rows]
        serializer = CustomerRoleSerializer(roles, many=True)
        return Response(serializer.data)
