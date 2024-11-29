# delivery_challan_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from app.serializers.VzPurchaseReport_serializers import DeliveryChallanSerializer
from app.models import DeliveryChallan

class DeliveryChallanReportView(APIView):
    def get(self, request):
        vetzone_id = request.query_params.get('vetzone_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not vetzone_id or not start_date or not end_date:
            return Response({"error": "vetzone_id, start_date, and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Adjust the query to your database schema if needed
        query = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY dc.created_date) AS sr_no,
                dc.created_date,
                dc.invoice_no,
                dc.invoice_amount,
                vz.name AS vetzone_name
            FROM delivery_challan dc
            JOIN vetzone vz ON vz.vetzone_id = dc.order_id  -- Adjust the join condition based on your actual schema
            WHERE vz.vetzone_id = %s
            AND dc.created_date BETWEEN %s AND %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [vetzone_id, start_date, end_date])
            result = cursor.fetchall()

        # Transform the result into a list of dictionaries
        data = [
            {
                "sr_no": row[0],
                "created_date": row[1],
                "invoice_no": row[2],
                "invoice_amount": row[3],
                "vetzone_name": row[4],
            }
            for row in result
        ]

        return Response(data, status=status.HTTP_200_OK)
