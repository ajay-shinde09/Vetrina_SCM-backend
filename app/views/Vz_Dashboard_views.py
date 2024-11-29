# # from rest_framework.response import Response
# # from rest_framework.views import APIView
# # from django.db import connection
# # from .Vz_Dashboard_serializers import OrderDetailsSerializer, ProductDetailsSerializer
# # from .models import Placeorder
# # from django.utils import timezone
# # from datetime import datetime
# # import pytz
# # ##################################################################################################
# # class OrderDetailsView(APIView):
# #     def get(self, request):
# #         # Get month and year from query parameters
# #         month: str = request.query_params.get('month', None)
# #         year: str = request.query_params.get('year', None)

# #         filters = {}

# #         # Prepare filter conditions based on month and year
# #         if month and year:
# #             start_year, end_year = map(int, year.split('-'))
# #             start_date = datetime(int(start_year), int(month), 1, tzinfo=pytz.utc)
# #             end_date = datetime(int(end_year - 1), 12, 31, 23, 59, 59, tzinfo=pytz.utc)
# #             date_range = [start_date, end_date]
# #             # Filter by month and year
# #             filters = {
# #                 'created_date__range': date_range,
# #                 'created_date__month': month
# #             }

# #         # Calculate counts for different order statuses
# #         # SELECT COUNT(*) FROM placeorder WHERE (status = 'p') AND (YEAR(created_date) = year) AND (MONTH(created_date) = month)

# #         counts = {
# #             'new_orders': Placeorder.objects.filter(**filters).count(),
# #             'pending_orders': Placeorder.objects.filter(status='P', **filters).count(),
# #             'inprocess_orders': Placeorder.objects.filter(status='I', **filters).count(),
# #             'dispatched_orders': Placeorder.objects.filter(status='Y', **filters).count(),
# #             'delivered_orders': Placeorder.objects.filter(status='D', **filters).count(),
# #             'cancelled_orders': Placeorder.objects.filter(status='N', **filters).count(),
# #         }

# #         # Get order_id if provided
# #         order_id = request.query_params.get('order_id', None)

# #         # Prepare the SQL query for order details with the subquery
# #         order_details_query = """
#             # SELECT 
#             #     subquery.stockiest_order_id AS order_no, 
#             #     v.name AS vetzone_name, 
#             #     h.hq_name AS headquarters, 
#             #     subquery.created_date AS order_date, 
#             #     subquery.total_amount AS amount, 
#             #     subquery.status
#             # FROM (
#             #     SELECT 
#             #         p.stockiest_order_id, 
#             #         p.created_date, 
#             #         p.status,
#             #         SUM(otp.rate * otp.quantity) AS total_amount,
#             #         otp.order_id
#             #     FROM 
#             #         placeorder p
#             #     JOIN 
#             #         order_table_product otp ON p.user_id = otp.user_id
#             #     WHERE 
#             #         p.status = 'P'
#             #     GROUP BY 
#             #         p.stockiest_order_id, p.created_date, p.status, otp.order_id
#             # ) AS subquery
#             # JOIN 
#             #     vetzone v ON subquery.order_id = v.vetzone_id
#             # JOIN 
#             #     vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id
#             # JOIN 
#             #     headquarters h ON vhd.hq_id = h.hq_id
# #             WHERE 
# #                 1=1
# #         """

# #         # If order_id is provided, filter the query by order_id
# #         query_params = []
# #         if order_id:
# #             order_details_query += " AND subquery.stockiest_order_id = %s"
# #             query_params.append(order_id)

# #         # Execute the first SQL query
# #         with connection.cursor() as cursor:
# #             cursor.execute(order_details_query, query_params)
# #             order_details_rows = cursor.fetchall()

# #         # Prepare the first set of data
# #         order_details_data = []
# #         for index, row in enumerate(order_details_rows, start=1):
# #             order_details_data.append({
# #                 'sr_no': index,
# #                 'order_no': row[0],
# #                 'vetzone_name': row[1],
# #                 'headquarters': row[2],
# #                 'order_date': row[3],
# #                 'amount': row[4],
# #                 'status': row[5],
# #             })

# #         # Prepare the base SQL query for the second part (product details) with the given stockiest_order_id
# #         product_details_query = """
# #             SELECT 
# #                 p.product_name AS product_name,
# #                 p.sku AS sku,
# #                 otp.quantity AS quantity,
# #                 otp.mrp AS mrp,
# #                 otp.rate AS rate,
# #                 otp.order_id AS order_id
# #             FROM 
# #                 order_table_product otp
# #             JOIN 
# #                 product p ON otp.product_id = p.product_id
# #             JOIN 
# #                 placeorder po ON po.stockiest_order_id = otp.order_id
# #             WHERE 
# #                 po.status = 'P'
# #         """

# #         # If order_id is provided, filter the query by order_id
# #         if order_id:
# #             product_details_query += " AND otp.order_id = %s"
# #             query_params = [order_id]
# #         else:
# #             query_params = []

# #         # Execute the second SQL query
# #         with connection.cursor() as cursor:
# #             cursor.execute(product_details_query, query_params)
# #             product_details_rows = cursor.fetchall()

# #         # Prepare the second set of data
# #         product_details_data = []
# #         for index, row in enumerate(product_details_rows, start=1):
# #             product_details_data.append({
# #                 'sr_no': index,
# #                 'product_name': row[0],
# #                 'sku': row[1],
# #                 'quantity': row[2],
# #                 'mrp': row[3],
# #                 'rate': row[4],
# #             })

# #         # Serialize the order details data
# #         order_serializer = OrderDetailsSerializer(data=order_details_data, many=True)
# #         order_serializer.is_valid(raise_exception=True)

# #         # Serialize the product details data
# #         product_serializer = ProductDetailsSerializer(data=product_details_data, many=True)
# #         product_serializer.is_valid(raise_exception=True)

# #         # Combine both serialized data
# #         combined_data = {
# #             'order_counts': counts,
# #             'order_details': order_serializer.data,
# #             'product_details': product_serializer.data,
# #         }

# #         return Response(combined_data)

# from rest_framework.views import APIView 
# from rest_framework.response import Response
# from django.db import connection
# from .models import Placeorder
# from django.utils import timezone
# from datetime import datetime
# import pytz

# class OrderAndProductDetailsView(APIView):
#     def get(self, request):
#         # Get month and year from query parameters
#         month = request.query_params.get('month', None)
#         year = request.query_params.get('year', None)
#         order_no = request.query_params.get('order_no', None)  # Fetching order_no
        
#         filters = {}
        
#         # Prepare filter conditions based on month and year
#         if month and year:
#             start_year, end_year = map(int, year.split('-'))
#             start_date = datetime(int(start_year), int(month), 1, tzinfo=pytz.utc)
#             end_date = datetime(int(end_year - 1), 12, 31, 23, 59, 59, tzinfo=pytz.utc)
#             filters = {
#                 'created_date__range': [start_date, end_date],
#                 'created_date__month': month
#             }
        
#         # Get the current date
#         current_date = timezone.now().date()

#         # Define the filter for new orders on the current date
#         new_order_filters = {
#             'created_date__date': current_date,  # Filter by current date
#             'user_role': 'VetZone',  # Filter by user role
#             'status': 'P'  # Filter by status 'P' (pending)
#         }

#         # Calculate counts for different order statuses
#         counts = {
#             'new_orders': Placeorder.objects.filter(**new_order_filters).count(),  # Current date filter applied here
#             'pending_orders': Placeorder.objects.filter(status='P', **filters).count(),
#             'inprocess_orders': Placeorder.objects.filter(status='I', **filters).count(),
#             'dispatched_orders': Placeorder.objects.filter(status='Y', **filters).count(),
#             'delivered_orders': Placeorder.objects.filter(status='D', **filters).count(),
#             'cancelled_orders': Placeorder.objects.filter(status='N', **filters).count(),
#         }

#         # If order_no is provided, fetch product details for that order
#         if order_no:
#             with connection.cursor() as cursor:
#                 product_query = """
#                     SELECT ROW_NUMBER() OVER (ORDER BY otp.order_product_id) AS sr_no,
#                            p.product_name,
#                            p.sku,
#                            otp.quantity,
#                            otp.mrp,
#                            otp.rate
#                     FROM order_table_product otp
#                     JOIN product p ON otp.product_id = p.product_id
#                     WHERE otp.order_id = %s;
#                 """
#                 cursor.execute(product_query, [order_no])
#                 product_result = cursor.fetchall()

#             product_data = [
#                 {
#                     'sr_no': row[0],
#                     'product_name': row[1],
#                     'sku': row[2],
#                     'quantity': row[3],
#                     'mrp': row[4],
#                     'rate': row[5],
#                 } for row in product_result
#             ]

#             return Response({
#                 'counts': counts,
#                 'order_no': order_no,
#                 'product_details': product_data
#             })

#         # Otherwise, fetch order details list
#         else:
#             with connection.cursor() as cursor:
#                 order_query = """
#                     SELECT 
#                 subquery.stockiest_order_id AS order_no, 
#                 v.name AS vetzone_name, 
#                 h.hq_name AS headquarters, 
#                 subquery.created_date AS order_date, 
#                 subquery.total_amount AS amount, 
#                 subquery.status
#             FROM (
#                 SELECT 
#                     p.stockiest_order_id, 
#                     p.created_date, 
#                     p.status,
#                     SUM(otp.rate * otp.quantity) AS total_amount,
#                     otp.order_id
#                 FROM 
#                     placeorder p
#                 JOIN 
#                     order_table_product otp ON p.user_id = otp.user_id
#                 WHERE 
#                     p.status = 'P'
#                 GROUP BY 
#                     p.stockiest_order_id, p.created_date, p.status, otp.order_id
#             ) AS subquery
#             JOIN 
#                 vetzone v ON subquery.order_id = v.vetzone_id
#             JOIN 
#                 vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id
#             JOIN 
#                 headquarters h ON vhd.hq_id = h.hq_id
#                 """
#                 cursor.execute(order_query)
#                 order_result = cursor.fetchall()

#             order_data = [
#                 {
#                     'sr_no': row[0],
#                     'order_no': row[1],
#                     'vetzone_name': row[2],
#                     'headquarter': row[3],
#                     'order_date': row[4],
#                     'order_amount': row[5],
#                     'status': row[6],
#                 } for row in order_result
#             ]

#             return Response({
#                 'counts': counts,
#                 'order_details': order_data
#             })
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from app.models import Placeorder
from django.utils import timezone
from datetime import datetime
import pytz

class OrderAndProductDetailsView(APIView):
    def get(self, request):
        # Get month and year from query parameters
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)
        order_no = request.query_params.get('order_no', None)  # Fetching order_no
        
        filters = {}
        
        # Prepare filter conditions based on month and year
        if month and year:
            start_year, end_year = map(int, year.split('-'))
            start_date = datetime(int(start_year), int(month), 1, tzinfo=pytz.utc)
            end_date = datetime(int(end_year - 1), 12, 31, 23, 59, 59, tzinfo=pytz.utc)
            filters = {
                'created_date__range': [start_date, end_date],
                'created_date__month': month
            }
        
        # Get the current date
        current_date = timezone.now().date()

        # Define the filter for new orders on the current date
        new_order_filters = {
            'created_date__date': current_date,  # Filter by current date
            'user_role': 'VetZone',  # Filter by user role
            'status': 'P'  # Filter by status 'P' (pending)
        }

        # Calculate counts for different order statuses
        counts = {
            'new_orders': Placeorder.objects.filter(**new_order_filters).count(),  # Current date filter applied here
            'pending_orders': Placeorder.objects.filter(status='P', **filters).count(),
            'inprocess_orders': Placeorder.objects.filter(status='I', **filters).count(),
            'dispatched_orders': Placeorder.objects.filter(status='Y', **filters).count(),
            'delivered_orders': Placeorder.objects.filter(status='D', **filters).count(),
            'cancelled_orders': Placeorder.objects.filter(status='N', **filters).count(),
        }

        # If order_no is provided, fetch product details for that order
        if order_no:
            with connection.cursor() as cursor:
                product_query = """
                    SELECT ROW_NUMBER() OVER (ORDER BY otp.order_product_id) AS sr_no,
                           p.product_name,
                           p.sku,
                           otp.quantity,
                           otp.mrp,
                           otp.rate
                    FROM order_table_product otp
                    JOIN product p ON otp.product_id = p.product_id
                    WHERE otp.order_id = %s;
                """
                cursor.execute(product_query, [order_no])
                product_result = cursor.fetchall()

            product_data = [
                {
                    'sr_no': row[0],
                    'product_name': row[1],
                    'sku': row[2],
                    'quantity': row[3],
                    'mrp': row[4],
                    'rate': row[5],
                } for row in product_result
            ]

            return Response({
                'counts': counts,
                'order_no': order_no,
                'product_details': product_data
            })

        # Otherwise, fetch order details list
        else:
            with connection.cursor() as cursor:
                order_query = """
                    SELECT 
                        subquery.stockiest_order_id AS order_no, 
                        v.name AS vetzone_name, 
                        h.hq_name AS headquarters, 
                        subquery.created_date AS order_date, 
                        subquery.total_amount AS amount, 
                        subquery.status
                    FROM (
                        SELECT 
                            p.stockiest_order_id, 
                            p.created_date, 
                            p.status,
                            SUM(otp.rate * otp.quantity) AS total_amount,
                            otp.order_id
                        FROM 
                            placeorder p
                        JOIN 
                            order_table_product otp ON p.user_id = otp.user_id
                        WHERE 
                            p.status = 'P'
                        GROUP BY 
                            p.stockiest_order_id, p.created_date, p.status, otp.order_id
                    ) AS subquery
                    JOIN 
                        vetzone v ON subquery.order_id = v.vetzone_id
                    JOIN 
                        vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id
                    JOIN 
                        headquarters h ON vhd.hq_id = h.hq_id;
                """
                cursor.execute(order_query)
                order_result = cursor.fetchall()

            order_data = [
                {
                    'order_no': row[0],
                    'vetzone_name': row[1],
                    'headquarter': row[2],
                    'order_date': row[3],
                    'order_amount': row[4],
                    'status': row[5],
                } for row in order_result
            ]

            return Response({
                'counts': counts,
                'order_details': order_data
            })

