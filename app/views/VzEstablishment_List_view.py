from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers.VzEstablishment_List_serializers import VzEstablishmentListSerializer

class VzEstablishmentListView(APIView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    v.name AS vetzone_name,
                    h.hq_name AS hq,
                    v.mobile_number AS contact_number
                FROM 
                    vetzone v
                JOIN 
                    vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id
                JOIN 
                    headquarters h ON vhd.hq_id = h.hq_id;
            """)
            rows = cursor.fetchall()

        # Add the serial number (SrNo) to each row
        data = [
            {
                "srno": index + 1,  # Serial number starts from 1
                "vetzone_name": row[0],
                "hq": row[1],
                "contact_number": row[2],
                "establishment": "Establish"  
            }
            for index, row in enumerate(rows)
        ]

        serializer = VzEstablishmentListSerializer(data, many=True)
        return Response(serializer.data)
