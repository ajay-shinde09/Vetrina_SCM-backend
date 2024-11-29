# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Supplier
# from .SupplierDropDown_serializers import SupplierDropDownSerializer

# class HeadquartersDropDownListView(APIView):
#     def get(self, request):
#         # Fetch all headquarters
#         Suppliers = Suppliers.objects.all()
        
#         # Serialize the headquarters data
#         serializer = SupplierDropDownSerializer(Suppliers, many=True)
        
#         # Return the serialized data
#         return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework import generics
from app.models import Suppliers
from app.serializers.SupplierDropDown_serializers import SupplierDropDownSerializer

class SuppliersDropdownView(generics.ListAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SupplierDropDownSerializer
