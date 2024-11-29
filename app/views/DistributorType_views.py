from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.DistributorType_serializers import DistributorTypeSerializer

class DistributorTypeDropdownView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT distributor_type_id, distributor_type FROM distributor_type")
            rows = cursor.fetchall()

        distributor_types = [{'distributor_type_id': row[0], 'distributor_type': row[1]} for row in rows]
        serializer = DistributorTypeSerializer(distributor_types, many=True)
        return Response(serializer.data)
