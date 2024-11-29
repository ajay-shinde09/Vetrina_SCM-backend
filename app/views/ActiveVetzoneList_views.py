# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.ActiveVetzoneList_serializers import ActiveVetzoneListSerializer

class ActiveVetzoneListView(APIView):

    def get(self, request):
        with connection.cursor() as cursor:
            query = '''
                SELECT
                    ROW_NUMBER() OVER() AS sr_no,
                    vz.vetzone_id,
                    vz.name,
                    vt.v_type_name,
                    vz.email,
                    vz.mobile_number,
                    vz.created_on,
                    vz.approval_status
                FROM
                    vetzone vz
                JOIN
                    vetzone_type vt ON vz.type = vt.v_type_id
                WHERE
                    vz.approval_status = 'Y'
            '''
            cursor.execute(query)
            results = cursor.fetchall()

            # Creating a list of dictionaries for serializer
            columns = ['sr_no', 'vetzone_id', 'name', 'v_type_name', 'email', 'mobile_number', 'created_on', 'approval_status']
            data = [dict(zip(columns, row)) for row in results]

        serializer = ActiveVetzoneListSerializer(data, many=True)
        return Response(serializer.data)
