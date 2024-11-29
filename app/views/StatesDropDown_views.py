from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.StatesDropDown_serializers import StateSerializer

class StateDropdownView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT state_id, state_name FROM state")
            rows = cursor.fetchall()

        states = [{'state_id': row[0], 'state_name': row[1]} for row in rows]
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)
