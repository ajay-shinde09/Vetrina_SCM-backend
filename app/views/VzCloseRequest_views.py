from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from app.models import Vetzone, VetzoneCloseRequest, Admin
from app.serializers.VzCloseRequest_serializers import VetzoneRemarkUpdateSerializer
from django.db import connection

class VetzoneRemarkUpdateView(generics.GenericAPIView):
    serializer_class = VetzoneRemarkUpdateSerializer

    def get_queryset(self):
        # Override this method to avoid the error.
        return Vetzone.objects.none()


    def patch(self, request, *args, **kwargs):
        vetzone_name = request.data.get('vetzone_name')

        try:
            # Find the vetzone by name
            vetzone = Vetzone.objects.get(name=vetzone_name)
        except Vetzone.DoesNotExist:
            return Response({"error": "Vetzone not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Validate and update the Vetzone record
        serializer = self.get_serializer(vetzone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Update the Vetzone fields

            # After a successful patch, update the approval_status to 'C'
            vetzone.approval_status = "C"
            vetzone.save()

            # Insert or update the record in the vetzone_close_request table
            VetzoneCloseRequest.objects.create(
                vetzone_id=vetzone.vetzone_id,  # ID of the Vetzone
                created_by='92',  # Admin ID passed in the request
                created_on=timezone.now().date(),  # Current date
                refund_amt='',  # Empty field for now
                document='',  # Empty field for now
                status='P'  # Default status as 'P'
            )

            return Response({"message": "Remark updated, approval_status set to 'C', and close request created."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        # SQL query to join Vetzone, VetzoneCloseRequest, and Admin tables to retrieve data
        query = '''
        SELECT 
    vcr.vetzone_id,
    v.name AS "VetZone Name",
    'Headquarters' AS hq,
    a.username AS "requested_by",
    v.created_on AS "requested_date",
    vcr.status
FROM 
    vetzone_close_request vcr
JOIN 
    vetzone v ON vcr.vetzone_id = v.vetzone_id
JOIN 
    admin a ON vcr.created_by = a.admin_id;

        '''

        # Execute the query and fetch the result
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        # Structure the result into a response format
        response_data = [
            {
                "sr_no": idx + 1,  # Sr. No starting from 1
                "vetzone_name": row[1],
                "hq": row[2],
                "requested_by": row[3],
                "requested_date": row[4],
                "status": row[5]
            }
            for idx, row in enumerate(result)
        ]

        return Response(response_data, status=status.HTTP_200_OK)

