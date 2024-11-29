from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import connection
from app.serializers.VzGoods_serializers import VetZoneGoodsSerializer

class VetZoneGoodsFormView(APIView):
    def get(self, request, vetzone_id):
        if not vetzone_id:
            return Response({"error": "vetzone_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    v.vetzone_id,
                    v.name AS vetzone_name,
                    vg.sim_number,
                    vg.opening_goods,
                    vg.machine,
                    vg.machine_file,
                    vg.furniture,
                    vg.furniture_file
                FROM 
                    vetzone v
                JOIN 
                    vetzone_goods vg ON v.vetzone_id = vg.vetzone_id
                WHERE 
                    v.vetzone_id = %s
            """, [vetzone_id])
            row = cursor.fetchone()
        
        if not row:
            return Response({"error": "No data found for the given vetzone_id"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            'vetzone_id': row[0],
            'vetzone_name': row[1],
            'sim_number': row[2],
            'opening_goods': row[3],
            'machine': row[4],
            'machine_file': row[5],
            'furniture': row[6],
            'furniture_file': row[7]
        }
        
        serializer = VetZoneGoodsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
