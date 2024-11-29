from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Headquarters
from app.serializers.HeadquartersDropDown_serializers import HeadquartersDropDownSerializer

class HeadquartersDropDownListView(APIView):
    def get(self, request):
        # Fetch all headquarters
        headquarters = Headquarters.objects.all()
        
        # Serialize the headquarters data
        serializer = HeadquartersDropDownSerializer(headquarters, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
