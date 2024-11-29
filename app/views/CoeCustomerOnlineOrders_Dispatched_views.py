import os
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.urls import reverse
from django.conf import settings 
from app.serializers.CoeCustomerOnlineOrders_Dispatched_serializers import CoeCustomerOnlineOrdersDispatchedserializers
from rest_framework import status
from urllib.parse import quote

# class CoeCustomerOnlineOrdersDispatchedListView(APIView):
#     def get(self, request):
#         with connection.cursor() as cursor:
#             query = """
#                 SELECT 
#                     p.stockiest_order_id AS OrderId,
#                     c.name AS customer_name,
#                     cr.role_name AS customer_role,
#                     p.created_date AS order_date,
#                     p.created_date AS dispatch_date,
#                     p.status AS status,
#                     lr.lrno AS lrno, -- Retrieve lrno from lr_details table
#                     lr.file AS file_path  -- This should contain only the filename
#                 FROM 
#                     placeorder p
#                 JOIN 
#                     customer c ON p.user_id = c.customer_id
#                 JOIN 
#                     customer_roles cr ON c.role = cr.cust_role_id
#                 LEFT JOIN 
#                     lr_details lr ON p.stockiest_order_id = lr.order_id  -- Join with lr_details table
#                 WHERE 
#                     p.status = 'Y' AND p.order_type = 'online';
#             """
#             cursor.execute(query)
#             rows = cursor.fetchall()

#             # Define the columns for dictionary conversion
#             columns = ["OrderId", "customer_name", "customer_role", "order_date", "dispatch_date", "status", "lrno", "file_path"]

#             # Add SrNo and dynamically generated action link using reverse()
#             data = []
#             for index, row in enumerate(rows):
#                 customer = dict(zip(columns, row))
#                 customer['sr_no'] = index + 1
#                 customer['action'] = {
#                     'link': reverse('COM_CustomerOrders_pending', args=[customer['OrderId']]),
#                     'view_update_lr': 'view_update_File'
#                 }
#                 if customer['file_path']:
#                     file_path = customer['file_path'].strip()
#                     customer['file_url'] = f"{settings.MEDIA_URL}lr_files/{file_path}"
#                 else:
#                     customer['file_url'] = None

#                 # Debugging statement to check the file URL
#                 print(f"File URL: {customer['file_url']} for OrderId: {customer['OrderId']}")

#                 data.append(customer)

#             # Serialize the entire data list
#             serializer = CoeCustomerOnlineOrdersDispatchedserializers(data=data, many=True)
#             serializer.is_valid(raise_exception=True)  # Validate the entire dataset at once

#             # Return the final response with serialized data
#             return Response(serializer.data, status=status.HTTP_200_OK)
from django.conf import settings

class CoeCustomerOnlineOrdersDispatchedListView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            query = """
                SELECT 
                    p.stockiest_order_id AS OrderId,
                    c.name AS customer_name,
                    cr.role_name AS customer_role,
                    p.created_date AS order_date,
                    p.created_date AS dispatch_date,
                    p.status AS status,
                    lr.lrno AS lrno,
                    lr.file AS file_path
                FROM 
                    placeorder p
                JOIN 
                    customer c ON p.user_id = c.customer_id
                JOIN 
                    customer_roles cr ON c.role = cr.cust_role_id
                LEFT JOIN 
                    lr_details lr ON p.stockiest_order_id = lr.order_id
                WHERE 
                    p.status = 'Y' AND p.order_type = 'online';
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            columns = ["OrderId", "customer_name", "customer_role", "order_date", "dispatch_date", "status", "lrno", "file_path"]
            data = []
            for index, row in enumerate(rows):
                customer = dict(zip(columns, row))
                customer['sr_no'] = index + 1
                customer['action'] = {
                    'link': reverse('COM_CustomerOrders_pending', args=[customer['OrderId']]),
                    'view_update_lr': 'view_update_File'
                }

                                # Sanitize the file path
                file_name = customer['file_path']
                if file_name:
                    # Remove null characters and whitespace
                    file_name = file_name.replace('\0', '').strip()
                    if file_name:  # Ensure file_name is not empty after cleaning
                        # Use quote to encode special characters in the file name
                        encoded_file_name = quote(file_name)
                        customer['file_url'] = request.build_absolute_uri(f"{settings.MEDIA_URL}lr_files/{encoded_file_name}")
                    else:
                        customer['file_url'] = None
                else:
                    customer['file_url'] = None

                customer['file_path'] = file_name  # Store the cleaned file name
            serializer = CoeCustomerOnlineOrdersDispatchedserializers(data=data, many=True)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self, request):
        order_id = request.data.get("order_id")
        new_lrno = request.data.get("lrno")

        if not order_id or not new_lrno:
            return Response(
                {"error": "Both order_id and new lrno are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform the update in lr_details table
        try:
            with connection.cursor() as cursor:
                cursor.execute("""UPDATE lr_details SET lrno = %s WHERE order_id = %s;""", [new_lrno, order_id])
                
            return Response({"message": "LR number updated successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Failed to update LR number.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
