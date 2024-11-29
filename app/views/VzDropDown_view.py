from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework import status

class VetZoneDropDownView(APIView):
    def get(self, request):
        try:
            # Query to fetch all VetZone IDs and names
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT vetzone_id, name 
                    FROM vetzone
                ''')
                
                vetzone_rows = cursor.fetchall()

                # Prepare the VetZone data for response
                vetzones = [
                    {"VetZone ID": row[0], "VetZone Name": row[1]} 
                    for row in vetzone_rows
                ]
            
            # Return the list of VetZones
            return Response(vetzones, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
