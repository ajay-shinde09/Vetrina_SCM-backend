from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Divisions  # Assuming the model for the 'divisions' table is named Divisions
from app.serializers.DivisionsDropDown_serializers import DivisionDropDownSerializer

class DivisionDropDownListView(APIView):
    def get(self, request):
        # Retrieve all divisions
        divisions = Divisions.objects.all()

        # Serialize the divisions
        serializer = DivisionDropDownSerializer(divisions, many=True)

        # Return the serialized data as JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)
