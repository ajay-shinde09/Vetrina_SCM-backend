import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.urls import reverse
from django.conf import settings 
from app.permissions import IsCommercialOperationExecutive,IsNonAdminUser
from app.serializers.CoeCustomerOnlineOrders_Inprocess_serializers import CoeCustomerLrUploadSerializer, CoeCustomerOnlineOrdersInprocessserializers
from rest_framework import status
from django.utils.text import slugify
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import os
import uuid
from django.utils.timezone import now
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from app.models import LrDetails 
import os
from django.utils.timezone import now
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.db import connection


class CoeCustomerOnlineOrdersInprocessListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsCommercialOperationExecutive,IsNonAdminUser] 
    def get(self, request):
        # Execute the raw SQL query
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    placeorder.stockiest_order_id AS order_id,
                    customer.name AS customer_name,
                    customer_roles.role_name AS customer_role,
                    placeorder.created_date AS order_date,
                    placeorder.status AS status
                FROM 
                    placeorder
                JOIN 
                    customer ON placeorder.user_id = customer.customer_id
                JOIN 
                    customer_roles ON customer.role = customer_roles.cust_role_id
                WHERE 
                    placeorder.status = 'I' AND
                placeorder.order_type = 'online'; 
            """)

            # Extract column names and build the result dictionary
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Add additional fields and serialize the results
        serialized_results = []
        for idx, customer in enumerate(results, start=1):
            # Add serial number and action link
            customer['sr_no'] = idx
            customer['action'] = {
                'link': reverse('Customer_invoice', args=[customer['order_id']]),
                'upload_lr': 'Upload File'  
            }
            
            # Serialize each customer entry
            serializer = CoeCustomerOnlineOrdersInprocessserializers(data=customer)
            serializer.is_valid(raise_exception=True)  # Validate data, raise an exception if invalid
            serialized_results.append(serializer.data)  # Add valid serialized data to results

        # Return the final response
        return Response(serialized_results)
    
    # def post(self, request):
    #     order_id = request.data.get('order_id')
    #     if not order_id:
    #         return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     serializer = CoeCustomerLrUploadSerializer(data=request.data)
    #     if serializer.is_valid():
    #         lr_number = serializer.validated_data['lr_number']
    #         receipt_file = serializer.validated_data['receipt_file']

    #         # Save the file to the media/lr_files directory
    #         lr_files_path = os.path.join(settings.MEDIA_ROOT, 'lr_files')
    #         os.makedirs(lr_files_path, exist_ok=True)
            
    #          # Create a new file name to avoid conflicts
    #         original_filename = slugify(receipt_file.name) 
    #         file_path = os.path.join(lr_files_path, original_filename)


    #         # Save the uploaded file
    #         with open(file_path, 'wb+') as destination:
    #             for chunk in receipt_file.chunks():
    #                 destination.write(chunk)

    #         # Insert the LR details into the database
    #         with connection.cursor() as cursor:
    #             cursor.execute("""
    #                 INSERT INTO lr_details (order_id, lrno, file)
    #                 VALUES (%s, %s, %s)
    #             """, [order_id, lr_number, original_filename])  # Adjust as needed

    #             cursor.execute("""
    #                 UPDATE placeorder
    #                 SET status = 'Y'
    #                 WHERE stockiest_order_id = %s AND status = 'I'
    #             """, [order_id])

    #         return Response({"message": "LR number and receipt file uploaded successfully"}, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CoeCustomerLrUploadSerializer(data=request.data)
        if serializer.is_valid():
            lr_number = serializer.validated_data['lr_number']
            receipt_file = serializer.validated_data['receipt_file']

            # Extract the original file name (without the full path)
            original_file_name = os.path.basename(receipt_file.name)

            # Define the binary file storage path
            lr_files_path = os.path.join(settings.MEDIA_ROOT, 'lr_files')
            os.makedirs(lr_files_path, exist_ok=True)
            binary_file_path = os.path.join(lr_files_path, original_file_name)

            # Save the file as binary in the `lr_files` folder
            with open(binary_file_path, 'wb') as destination:
                for chunk in receipt_file.chunks():
                    destination.write(chunk)

            # Save only the original file name in the database
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO lr_details (order_id, lrno, file, is_verified, dispatch_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, [order_id, lr_number, original_file_name, 'N', now()])

                # Update the status in `placeorder` table
                cursor.execute("""
                    UPDATE placeorder
                    SET status = 'Y'
                    WHERE stockiest_order_id = %s AND status = 'I'
                """, [order_id])

            return Response({"message": "LR number and receipt file uploaded successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
