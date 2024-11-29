from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.serializers.BatchDropDown_serializers import BatchDropdownSerializer
from rest_framework import status

class BatchDropdownAPIView(APIView):
    def get(self, request, product_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.batch, i.quantity, i.pts AS Rate, i.mrp AS MRP
                FROM batch b
                JOIN instock i ON b.batch_id = i.batch_id
                WHERE b.product_id = %s
            """, [product_id])
            results = cursor.fetchall()
        
        if not results:
            return Response({"detail": "No batches found for this product."}, status=status.HTTP_404_NOT_FOUND)
        
        # Format and prepare data for serialization
        data = [
            {
                "batch_qty": f"{batch} ({quantity})",
                "product_id": product_id,
                "Rate": Rate,
                "MRP": MRP,
            }
            for batch, quantity, Rate, MRP in results
        ]

        # Serialize the data
        serializer = BatchDropdownSerializer(data=data, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
