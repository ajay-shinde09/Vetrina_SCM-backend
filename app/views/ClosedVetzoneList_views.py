from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.ClosedVetzoneList_serializers import VetzoneSerializer

class ClosedVetzoneListView(APIView):

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            query = """
            SELECT 
    v.vetzone_id,
    v.name,
    vt.v_type_name,
    v.email,
    v.mobile_number,
    vcr.created_on AS created_on, 
    vcr.created_on AS closed_on,  -- Assuming closed_on is the created_on from vetzone_close_request
    v.remark,
    v.approval_status
FROM 
    vetzone v
JOIN 
    vetzone_type vt ON v.type = vt.v_type_id
JOIN 
    vetzone_close_request vcr ON v.vetzone_id = vcr.vetzone_id  -- Adjust the join condition as necessary
WHERE 
    v.approval_status = 'C';

            """
            cursor.execute(query)
            results = cursor.fetchall() 

        columns = ['sr_no', 'vetzone_id', 'name', 'v_type_name', 'email', 'mobile_number', 'created_on', 'closed_on', 'remark', 'approval_status']
        data = [
    {
        'srno': index + 1,  # Use srno instead of sr_no
        'vetzone_id': row[0],
        'name': row[1],
        'v_type_name': row[2],
        'email': row[3],
        'mobile_number': row[4],
        'created_on': row[5],
        'closed_on': row[6],
        'remark': row[7],
        'approval_status': row[8]
    } for index, row in enumerate(results)
]

    
        # Serialize the data and return the response
        serializer = VetzoneSerializer(data, many=True)
        return Response(serializer.data)
