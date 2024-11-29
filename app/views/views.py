# from django.http import JsonResponse
# from django.views import View
# from django.db import connection
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# import json
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# # Custom method to extract and validate JWT token
# def get_user_from_token(request):
#     """
#     Extracts user_id and role_name from the access token in the Authorization header.
#     """
#     auth = JWTAuthentication()
#     try:
#         token = request.headers.get('Authorization', '').split(' ')[1]
#         validated_token = auth.get_validated_token(token)
#         user_id = validated_token.get('customer_id')
#         role_name = validated_token.get('role_name')
#         if not user_id or not role_name:
#             return None, None
#         return user_id, role_name
#     except (InvalidToken, TokenError, IndexError):
#         return None, None

# @method_decorator(csrf_exempt, name='dispatch')
# class ProductsByDivision(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             # Authenticate user
#             user_id, role_name = get_user_from_token(request)
#             if not user_id or not role_name:
#                 return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

#             # Parse JSON payload from the request
#             body = json.loads(request.body)
#             division_name = body.get('division_name')

#             if not division_name:
#                 return JsonResponse({'error': 'division_name is required'}, status=400)

#             # Query to get division_id based on division_name
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT division_id FROM divisions WHERE division_name = %s", [division_name])
#                 division = cursor.fetchone()

#                 if not division:
#                     return JsonResponse({'error': f'Division "{division_name}" not found'}, status=404)

#                 division_id = division[0]

#                 # Query to get product details and 3_months_avg_sale calculation from only the product table
#                 cursor.execute("""
#                     SELECT 
#                         p.product_name, 
#                         p.sku, 
#                         COALESCE(i.quantity, 0) AS quantity, 
#                         COALESCE(i.mrp, 0) AS mrp, 
#                         COALESCE(i.pts, 0) AS pts, 
#                         COALESCE(i.ptr, 0) AS ptr, 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
#                         COALESCE(ROUND(SUM(otp.quantity) / 3, 2), 0) AS three_months_avg_sale
#                     FROM product p
#                     LEFT JOIN instock i ON p.product_id = i.product_id
#                     LEFT JOIN order_table_product otp ON p.product_id = otp.product_id
#                     WHERE p.product_division = %s
#                     GROUP BY 
#                         p.product_id, p.product_name, p.sku, i.quantity, i.mrp, i.pts, i.ptr, 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty
#                 """, [division_id])

#                 products = cursor.fetchall()

#             # Format the response
#             product_list = [
#                 {
#                     'product_name': product[0],
#                     'sku': product[1],
#                     'quantity': product[2],
#                     'mrp': product[3],
#                     'pts': product[4],
#                     'ptr': product[5],
#                     'scheme_lot_1': f"Inv. qnty: {product[6]}, Free qnty: {product[7]}",
#                     'scheme_lot_2': f"Inv. qnty: {product[8]}, Free qnty: {product[9]}",
#                     'three_months_avg_sale': product[10]
#                 }
#                 for product in products
#             ]

#             return JsonResponse({'division_name': division_name, 'products': product_list}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

# @method_decorator(csrf_exempt, name='dispatch')
# class ProductDetails(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             # Authenticate user
#             user_id, role_name = get_user_from_token(request)
#             if not user_id or not role_name:
#                 return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

#             # Get product_id from query parameters
#             product_id = request.GET.get('product_id')

#             if not product_id:
#                 return JsonResponse({'error': 'product_id is required'}, status=400)

#             # Query to fetch product details including category_name
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         p.product_name, 
#                         p.sku, 
#                         COALESCE(i.quantity, 0) AS quantity, 
#                         COALESCE(i.mrp, 0) AS mrp, 
#                         COALESCE(i.pts, 0) AS pts, 
#                         COALESCE(i.ptr, 0) AS ptr, 
#                         p.sheme_lot_one_invoice_qnty, 
#                         p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, 
#                         p.sheme_lot_two_free_qnty,
#                         COALESCE(ROUND(SUM(otp.quantity) / 3, 2), 0) AS three_months_avg_sale,
#                         pc.category_name
#                     FROM product p
#                     LEFT JOIN instock i ON p.product_id = i.product_id
#                     LEFT JOIN order_table_product otp ON p.product_id = otp.product_id
#                     LEFT JOIN product_category pc ON p.category_id = pc.category_id
#                     WHERE p.product_id = %s
#                     GROUP BY 
#                         p.product_id, p.product_name, p.sku, i.quantity, i.mrp, i.pts, i.ptr, 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
#                         pc.category_name
#                 """, [product_id])

#                 product = cursor.fetchone()

#                 if not product:
#                     return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)

#             # Format the response
#             product_details = {
#                 'product_name': product[0],
#                 'sku': product[1],
#                 'quantity': product[2],
#                 'mrp': product[3],
#                 'pts': product[4],
#                 'ptr': product[5],
#                 'scheme_lot_1': f"Inv. qnty: {product[6]}, Free qnty: {product[7]}",
#                 'scheme_lot_2': f"Inv. qnty: {product[8]}, Free qnty: {product[9]}",
#                 'three_months_avg_sale': product[10],
#                 'category_name': product[11]
#             }

#             return JsonResponse({'product': product_details}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

# @method_decorator(csrf_exempt, name='dispatch')
# class CalculateLotDetails(View):
#     def post(self, request, *args, **kwargs):
#         try:
#             # Authenticate user
#             user_id, role_name = get_user_from_token(request)
#             if not user_id or not role_name:
#                 return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

#             # Parse JSON payload from the request
#             body = json.loads(request.body)
#             product_id = body.get('product_id')
#             selected_lot = body.get('selected_lot')  # "lot_1" or "lot_2"
#             inv_qnty = body.get('inv_qnty')  # Provided inventory quantity
#             free_qnty = body.get('free_qnty')  # Provided free quantity

#             if not product_id or not selected_lot:
#                 return JsonResponse({'error': 'product_id and selected_lot are required'}, status=400)

#             # Fetch product details from the database
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
#                         i.mrp, i.pts, i.ptr
#                     FROM product p
#                     LEFT JOIN instock i ON p.product_id = i.product_id
#                     WHERE p.product_id = %s
#                 """, [product_id])

#                 product = cursor.fetchone()

#                 if not product:
#                     return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)

#             # Extract product details
#             lot_1_inv_qnty, lot_1_free_qnty, lot_2_inv_qnty, lot_2_free_qnty, mrp, pts, ptr = product

#             # Calculate based on the selected lot
#             if selected_lot == 'lot_1':
#                 inv_qnty += lot_1_inv_qnty
#                 free_qnty += lot_1_free_qnty
#             elif selected_lot == 'lot_2':
#                 inv_qnty += lot_2_inv_qnty
#                 free_qnty += lot_2_free_qnty
#             else:
#                 return JsonResponse({'error': 'Invalid selected_lot. Choose either "lot_1" or "lot_2"'})


#             total_value = inv_qnty * mrp + free_qnty * pts
#             ptr_value = inv_qnty * ptr + free_qnty * pts

#             # Calculate sales potential
#             sales_potential = total_value - ptr_value

#             return JsonResponse({
#                 'product_id': product_id,
#                 'lot_selected': selected_lot,
#                 'final_invoice_qnty': inv_qnty,
#                 'final_free_qnty': free_qnty,
#                 'total_value': total_value,
#                 'ptr_value': ptr_value,
#                 'sales_potential': sales_potential
#             }, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)



# from django.http import JsonResponse
# from django.views import View
# from django.db import connection
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import IsAuthenticated
# # from rest_framework.authentication import JWTAuthentication
# import json
# from app.permissions import IsCnF, IsCustomer, IsStockiest,IsKeyAccount,IsRetailer,IsPetShop,IsFarmer,IsDoctor,IsLSS,IsPetOwner
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class ProductsByDivision(View):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated|IsCustomer|IsCnF | IsStockiest|IsKeyAccount|IsRetailer|IsPetShop|IsFarmer|IsDoctor|IsLSS|IsPetOwner]
 
#     @method_decorator(csrf_exempt, name='dispatch')
#     def post(self, request, *args, **kwargs):
#         try:
#             # Parse JSON payload from the request
#             body = json.loads(request.body)
#             division_name = body.get('division_name')
 
#             if not division_name:
#                 return JsonResponse({'error': 'division_name is required'}, status=400)
 
#             # Query to get division_id based on division_name
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT division_id FROM divisions WHERE division_name = %s", [division_name])
#                 division = cursor.fetchone()
 
#                 if not division:
#                     return JsonResponse({'error': f'Division "{division_name}" not found'}, status=404)
 
#                 division_id = division[0]
 
#                 # Query to get product details and 3_months_avg_sale calculation from only the product table
#                 cursor.execute("""
#                     SELECT 
#                         p.product_name, 
#                         p.sku, 
#                         COALESCE(i.quantity, 0) AS quantity, 
#                         COALESCE(i.mrp, 0) AS mrp, 
#                         COALESCE(i.pts, 0) AS pts, 
#                         COALESCE(i.ptr, 0) AS ptr, 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
#                         COALESCE(ROUND(SUM(otp.quantity) / 3, 2), 0) AS three_months_avg_sale
#                     FROM product p
#                     LEFT JOIN instock i ON p.product_id = i.product_id
#                     LEFT JOIN order_table_product otp ON p.product_id = otp.product_id
#                     WHERE p.product_division = %s
#                     GROUP BY 
#                         p.product_id, p.product_name, p.sku, i.quantity, i.mrp, i.pts, i.ptr, 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty
#                 """, [division_id])
 
#                 products = cursor.fetchall()
 
#             # Format the response
#             product_list = [
#                 {
#                     'product_name': product[0],
#                     'sku': product[1],
#                     'quantity': product[2],
#                     'mrp': product[3],
#                     'pts': product[4],
#                     'ptr': product[5],
#                     'scheme_lot_1': f"Inv. qnty: {product[6]}, Free qnty: {product[7]}",
#                     'scheme_lot_2': f"Inv. qnty: {product[8]}, Free qnty: {product[9]}",
#                     'three_months_avg_sale': product[10]
#                 }
#                 for product in products
#             ]
 
#             # Calculate the total amount (sum of all product prices)
#             total_amount = sum([product[3] * product[2] for product in products])
 
#             return JsonResponse({'division_name': division_name, 'products': product_list, 'total_amount': total_amount}, status=200)
 
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
 
 
# class ProductDetails(View):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
 
#     @method_decorator(csrf_exempt, name='dispatch')
#     def get(self, request, *args, **kwargs):
#         try:
#             # Get product_id from query parameters
#             product_id = request.GET.get('product_id')
 
#             if not product_id:
#                 return JsonResponse({'error': 'product_id is required'}, status=400)
 
#             # Query to fetch product details including category_name
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         p.product_name, 
#                         p.sku, 
#                         COALESCE(i.quantity, 0) AS quantity, 
#                         COALESCE(i.mrp, 0) AS mrp, 
#                         COALESCE(i.pts, 0) AS pts, 
#                         COALESCE(i.ptr, 0) AS ptr, 
#                         p.sheme_lot_one_invoice_qnty, 
#                         p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, 
#                         p.sheme_lot_two_free_qnty,
#                         COALESCE(ROUND(SUM(otp.quantity) / 3, 2), 0) AS three_months_avg_sale,
#                         pc.category_name
#                     FROM product p
#                     LEFT JOIN instock i ON p.product_id = i.product_id
#                     LEFT JOIN order_table_product otp ON p.product_id = otp.product_id
#                     LEFT JOIN product_category pc ON p.category_id = pc.category_id
#                     WHERE p.product_id = %s
#                     GROUP BY 
#                         p.product_id, p.product_name, p.sku, i.quantity, i.mrp, i.pts, i.ptr, 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
#                         pc.category_name
#                 """, [product_id])
 
#                 product = cursor.fetchone()
 
#                 if not product:
#                     return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)
 
#             # Format the response
#             product_details = {
#                 'product_name': product[0],
#                 'sku': product[1],
#                 'quantity': product[2],
#                 'mrp': product[3],
#                 'pts': product[4],
#                 'ptr': product[5],
#                 'scheme_lot_1': f"Inv. qnty: {product[6]}, Free qnty: {product[7]}",
#                 'scheme_lot_2': f"Inv. qnty: {product[8]}, Free qnty: {product[9]}",
#                 'three_months_avg_sale': product[10],
#                 'category_name': product[11]
#             }
 
#             return JsonResponse({'product': product_details}, status=200)
 
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
 
 
# class CalculateLotDetails(View):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
 
#     @method_decorator(csrf_exempt, name='dispatch')
#     def post(self, request, *args, **kwargs):
#         try:
#             # Parse JSON payload from the request
#             body = json.loads(request.body)
#             product_id = body.get('product_id')
#             selected_lot = body.get('selected_lot')  # "lot_1" or "lot_2"
#             inv_qnty = body.get('inv_qnty')  # Provided inventory quantity
#             free_qnty = body.get('free_qnty')  # Provided free quantity
 
#             if not product_id or not selected_lot:
#                 return JsonResponse({'error': 'product_id and selected_lot are required'}, status=400)
 
#             # Fetch product details from the database
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT 
#                         p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
#                         p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
#                         i.mrp, i.pts, i.ptr
#                     FROM product p
#                     LEFT JOIN instock i ON p.product_id = i.product_id
#                     WHERE p.product_id = %s
#                 """, [product_id])
 
#                 product = cursor.fetchone()
 
#                 if not product:
#                     return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)
 
#             # Extract product details
#             lot_1_inv_qnty, lot_1_free_qnty, lot_2_inv_qnty, lot_2_free_qnty, mrp, pts, ptr = product
 
#             # Convert all Decimal values to float for calculations
#             lot_1_inv_qnty = float(lot_1_inv_qnty or 0)
#             lot_1_free_qnty = float(lot_1_free_qnty or 0)
#             lot_2_inv_qnty = float(lot_2_inv_qnty or 0)
#             lot_2_free_qnty = float(lot_2_free_qnty or 0)
#             mrp = float(mrp or 0)
#             pts = float(pts or 0)
#             ptr = float(ptr or 0)
 
#             # Adjust lot details based on selected_lot
#             if selected_lot == 'lot_1':
#                 adjusted_inv_qnty = lot_1_inv_qnty + inv_qnty
#                 adjusted_free_qnty = lot_1_free_qnty + free_qnty
#             elif selected_lot == 'lot_2':
#                 adjusted_inv_qnty = lot_2_inv_qnty + inv_qnty
#                 adjusted_free_qnty = lot_2_free_qnty + free_qnty
#             else:
#                 return JsonResponse({'error': 'Invalid selected_lot value. Use "lot_1" or "lot_2".'}, status=400)
 
#             # Return updated details
#             return JsonResponse({
#                 'product_id': product_id,
#                 'selected_lot': selected_lot,
#                 'adjusted_inv_qnty': adjusted_inv_qnty,
#                 'adjusted_free_qnty': adjusted_free_qnty,
#                 'mrp': mrp,
#                 'pts': pts,
#                 'ptr': ptr
#             }, status=200)
 
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)



from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json

class ProductsByDivision(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            body = request.data
            division_name = body.get('division_name')

            if not division_name:
                return JsonResponse({'error': 'division_name is required'}, status=400)

            with connection.cursor() as cursor:
                cursor.execute("SELECT division_id FROM divisions WHERE division_name = %s", [division_name])
                division = cursor.fetchone()

                if not division:
                    return JsonResponse({'error': f'Division "{division_name}" not found'}, status=404)

                division_id = division[0]

                cursor.execute("""
                    SELECT 
                        p.product_name, 
                        p.sku, 
                        COALESCE(CAST(i.quantity AS DECIMAL), 0) AS quantity, 
                        COALESCE(CAST(i.mrp AS DECIMAL), 0) AS mrp, 
                        COALESCE(i.pts, 0) AS pts, 
                        COALESCE(i.ptr, 0) AS ptr, 
                        p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
                        p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
                        COALESCE(ROUND(SUM(otp.quantity) / 3, 2), 0) AS three_months_avg_sale
                    FROM product p
                    LEFT JOIN instock i ON p.product_id = i.product_id
                    LEFT JOIN order_table_product otp ON p.product_id = otp.product_id
                    WHERE p.product_division = %s
                    GROUP BY 
                        p.product_id, p.product_name, p.sku, i.quantity, i.mrp, i.pts, i.ptr, 
                        p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
                        p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty
                """, [division_id])

                products = cursor.fetchall()

            product_list = [
                {
                    'product_name': product[0],
                    'sku': product[1],
                    'quantity': product[2],
                    'mrp': product[3],
                    'pts': product[4],
                    'ptr': product[5],
                    'scheme_lot_1': f"Inv. qnty: {product[6]}, Free qnty: {product[7]}",
                    'scheme_lot_2': f"Inv. qnty: {product[8]}, Free qnty: {product[9]}",
                    'three_months_avg_sale': product[10]
                }
                for product in products
            ]

            # Calculate the total amount
            try:
                total_amount = sum([float(product[3]) * float(product[2]) for product in products])
            except ValueError as e:
                return JsonResponse({'error': f'Invalid data in products: {str(e)}'}, status=500)

            return JsonResponse({'division_name': division_name, 'products': product_list, 'total_amount': total_amount}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class CalculateLotDetails(View):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
 
    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON payload from the request
            body = json.loads(request.body)
            product_id = body.get('product_id')
            selected_lot = body.get('selected_lot')  # "lot_1" or "lot_2"
            inv_qnty = body.get('inv_qnty')  # Provided inventory quantity
            free_qnty = body.get('free_qnty')  # Provided free quantity
 
            if not product_id or not selected_lot:
                return JsonResponse({'error': 'product_id and selected_lot are required'}, status=400)
 
            # Fetch product details from the database
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
                        p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
                        i.mrp, i.pts, i.ptr
                    FROM product p
                    LEFT JOIN instock i ON p.product_id = i.product_id
                    WHERE p.product_id = %s
                """, [product_id])
 
                product = cursor.fetchone()
 
                if not product:
                    return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)
 
            # Extract product details
            lot_1_inv_qnty, lot_1_free_qnty, lot_2_inv_qnty, lot_2_free_qnty, mrp, pts, ptr = product
 
            # Convert all Decimal values to float for calculations
            lot_1_inv_qnty = float(lot_1_inv_qnty or 0)
            lot_1_free_qnty = float(lot_1_free_qnty or 0)
            lot_2_inv_qnty = float(lot_2_inv_qnty or 0)
            lot_2_free_qnty = float(lot_2_free_qnty or 0)
            mrp = float(mrp or 0)
            pts = float(pts or 0)
            ptr = float(ptr or 0)
 
            # Adjust lot details based on selected_lot
            if selected_lot == 'lot_1':
                adjusted_inv_qnty = lot_1_inv_qnty + inv_qnty
                adjusted_free_qnty = lot_1_free_qnty + free_qnty
            elif selected_lot == 'lot_2':
                adjusted_inv_qnty = lot_2_inv_qnty + inv_qnty
                adjusted_free_qnty = lot_2_free_qnty + free_qnty
            else:
                return JsonResponse({'error': 'Invalid selected_lot value. Use "lot_1" or "lot_2".'}, status=400)
 
            # Return updated details
            return JsonResponse({
                'product_id': product_id,
                'selected_lot': selected_lot,
                'adjusted_inv_qnty': adjusted_inv_qnty,
                'adjusted_free_qnty': adjusted_free_qnty,
                'mrp': mrp,
                'pts': pts,
                'ptr': ptr
            }, status=200)
 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class ProductDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get(self, request, *args, **kwargs):
        try:
            # Get product_id from query parameters
            product_id = request.GET.get('product_id')
 
            if not product_id:
                return JsonResponse({'error': 'product_id is required'}, status=400)
 
            # Query to fetch product details including category_name
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.product_name, 
                        p.sku, 
                        COALESCE(i.quantity, 0) AS quantity, 
                        COALESCE(i.mrp, 0) AS mrp, 
                        COALESCE(i.pts, 0) AS pts, 
                        COALESCE(i.ptr, 0) AS ptr, 
                        p.sheme_lot_one_invoice_qnty, 
                        p.sheme_lot_one_free_qnty,
                        p.sheme_lot_two_invoice_qnty, 
                        p.sheme_lot_two_free_qnty,
                        COALESCE(ROUND(SUM(otp.quantity) / 3, 2), 0) AS three_months_avg_sale,
                        pc.category_name
                    FROM product p
                    LEFT JOIN instock i ON p.product_id = i.product_id
                    LEFT JOIN order_table_product otp ON p.product_id = otp.product_id
                    LEFT JOIN product_category pc ON p.category_id = pc.category_id
                    WHERE p.product_id = %s
                    GROUP BY 
                        p.product_id, p.product_name, p.sku, i.quantity, i.mrp, i.pts, i.ptr, 
                        p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
                        p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
                        pc.category_name
                """, [product_id])
 
                product = cursor.fetchone()
 
                if not product:
                    return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)
 
            # Format the response
            product_details = {
                'product_name': product[0],
                'sku': product[1],
                'quantity': product[2],
                'mrp': product[3],
                'pts': product[4],
                'ptr': product[5],
                'scheme_lot_1': f"Inv. qnty: {product[6]}, Free qnty: {product[7]}",
                'scheme_lot_2': f"Inv. qnty: {product[8]}, Free qnty: {product[9]}",
                'three_months_avg_sale': product[10],
                'category_name': product[11]
            }
 
            return JsonResponse({'product': product_details}, status=200)
 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
 
 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from django.db import connection

class CalculateLotDetails(APIView):
    # Configure authentication and permissions
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON payload from the request
            body = request.data  # DRF automatically parses JSON
            product_id = body.get('product_id')
            selected_lot = body.get('selected_lot')  # "lot_1" or "lot_2"
            inv_qnty = body.get('inv_qnty')  # Provided inventory quantity
            free_qnty = body.get('free_qnty')  # Provided free quantity
            
            # Validate required fields
            if not product_id or not selected_lot:
                return JsonResponse({'error': 'product_id and selected_lot are required'}, status=400)

            # Fetch product details from the database
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.sheme_lot_one_invoice_qnty, p.sheme_lot_one_free_qnty,
                        p.sheme_lot_two_invoice_qnty, p.sheme_lot_two_free_qnty,
                        i.mrp, i.pts, i.ptr
                    FROM product p
                    LEFT JOIN instock i ON p.product_id = i.product_id
                    WHERE p.product_id = %s
                """, [product_id])

                product = cursor.fetchone()

                if not product:
                    return JsonResponse({'error': f'Product with ID "{product_id}" not found'}, status=404)

            # Extract product details
            lot_1_inv_qnty, lot_1_free_qnty, lot_2_inv_qnty, lot_2_free_qnty, mrp, pts, ptr = product

            # Convert all Decimal or None values to float for calculations
            lot_1_inv_qnty = float(lot_1_inv_qnty or 0)
            lot_1_free_qnty = float(lot_1_free_qnty or 0)
            lot_2_inv_qnty = float(lot_2_inv_qnty or 0)
            lot_2_free_qnty = float(lot_2_free_qnty or 0)
            mrp = float(mrp or 0)
            pts = float(pts or 0)
            ptr = float(ptr or 0)

            # Adjust lot details based on selected_lot
            inv_qnty = float(inv_qnty or 0)
            free_qnty = float(free_qnty or 0)

            if selected_lot == 'lot_1':
                adjusted_inv_qnty = lot_1_inv_qnty + inv_qnty
                adjusted_free_qnty = lot_1_free_qnty + free_qnty
            elif selected_lot == 'lot_2':
                adjusted_inv_qnty = lot_2_inv_qnty + inv_qnty
                adjusted_free_qnty = lot_2_free_qnty + free_qnty
            else:
                return JsonResponse({'error': 'Invalid selected_lot value. Use "lot_1" or "lot_2".'}, status=400)

            # Return updated details
            return JsonResponse({
                'product_id': product_id,
                'selected_lot': selected_lot,
                'adjusted_inv_qnty': adjusted_inv_qnty,
                'adjusted_free_qnty': adjusted_free_qnty,
                'mrp': mrp,
                'pts': pts,
                'ptr': ptr
            }, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


