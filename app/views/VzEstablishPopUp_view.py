
# # # views.py
# # from rest_framework import status
# # from rest_framework.response import Response
# # from rest_framework.views import APIView
# # from .models import VetzoneGoods
# # from .VzEstablishPopUp_serializers import EstablishmentPopupSerializer

# # class EstablishmentPopupView(APIView):
# #      def post(self, request, *args, **kwargs):
# #         serializer = EstablishmentPopupSerializer(data=request.data, context={'request': request})
        
# #         if serializer.is_valid():
# #             # Handle file uploads
# #             files = request.FILES
# #             if 'machine_file' in files:
# #                 serializer.validated_data['machine_file'] = files['machine_file'].name
# #             if 'furniture_file' in files:
# #                 serializer.validated_data['furniture_file'] = files['furniture_file'].name

# #             # Save data
# #             instance = serializer.save()

# #             return Response({"message": "Establishment details updated successfully."}, status=status.HTTP_200_OK)
        
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # views.py
# # views.py
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .models import VetzoneGoods
# from .VzEstablishPopUp_serializers import EstablishmentPopupSerializer

# class EstablishmentPopupView(APIView):
#     def get(self, request, *args, **kwargs):
#         # Retrieve all VetzoneGoods entries (or add filtering as needed)
#         vetzone_goods = VetzoneGoods.objects.all()

#         # Serialize the data
#         serializer = EstablishmentPopupSerializer(vetzone_goods, many=True)

#         # Return the serialized data as the response
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = EstablishmentPopupSerializer(data=request.data, context={'request': request})
        
#         if serializer.is_valid():
#             # Handle file uploads
#             files = request.FILES
            
#             machine_file = files.get('machine_file', None)
#             furniture_file = files.get('furniture_file', None)

#             # Update the validated data with file names
#             validated_data = serializer.validated_data
#             if machine_file:
#                 validated_data['machine_file'] = machine_file.name
#             if furniture_file:
#                 validated_data['furniture_file'] = furniture_file.name

#             # Save the validated data to the database
#             instance = VetzoneGoods.objects.create(**validated_data)

#             return Response({"message": "Establishment details updated successfully."}, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers.VzEstablishPopUp_serializers import EstablishmentPopupSerializer

class EstablishmentPopupDataView(APIView):
    def get(self, request, vetzone_id, *args, **kwargs):
        try:
            vetzone_id = int(vetzone_id)
        except ValueError:
            return Response({"error": "Invalid vetzone_id"}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    v.vetzone_id, 
                    v.name AS vetzone_name
                FROM 
                    vetzone v
                WHERE 
                    v.vetzone_id = %s
            """, [vetzone_id])
            row = cursor.fetchone()

        if row:
            data = {
                "vetzone_id": row[0],
                "vetzone_name": row[1],
                "sim_number": None,
                "opening_goods": None,
                "machine": None,
                "machine_file": None,
                "furniture": None,
                "furniture_file": None
            }

            serializer = EstablishmentPopupSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Vetzone not found"}, status=status.HTTP_404_NOT_FOUND)

