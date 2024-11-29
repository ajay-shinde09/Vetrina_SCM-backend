# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes, authentication_classes
# from rest_framework import status
# from django.db import connection

# @api_view(['DELETE'])
# @authentication_classes([])  # No authentication required
# @permission_classes([])  # No permissions required
# def delete_order_product(request, order_product_id):  
#     try:
#         # Check if the product entry exists in order_table_product
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT order_id FROM order_table_product WHERE order_product_id = %s", [order_product_id]
#             )
#             product_entry = cursor.fetchone()
        
#         if not product_entry:
#             return Response(
#                 {"error": "Product entry not found in order_table_product."},
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         order_id = product_entry[0]

#         # Delete the product entry from order_table_product
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "DELETE FROM order_table_product WHERE order_product_id = %s", [order_product_id]
#             )
        
#         # Check if there are any remaining products for this order_id
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "SELECT COUNT(*) FROM order_table_product WHERE order_id = %s", [order_id]
#             )
#             remaining_count = cursor.fetchone()[0]
        
#         if remaining_count == 0:
#             # If no products left, update the status in the placeorder table
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "UPDATE placeorder SET status = 'D' WHERE stockiest_order_id = %s", [order_id]
#                 )

#         return Response(
#             {"message": "Product entry deleted from order_table_product. PlaceOrder status updated (if applicable)."},
#             status=status.HTTP_200_OK
#         )

#     except Exception as e:
#         return Response(
#             {"error": f"An error occurred: {str(e)}"},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )



from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class DeleteProduct(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_user_from_token(self, request):
        """
        Extracts user_id and role_name from the access token in the Authorization header.
        """
        auth = JWTAuthentication()
        try:
            token = request.headers.get('Authorization', '').split(' ')[1]
            validated_token = auth.get_validated_token(token)
            user_id = validated_token.get('customer_id')
            role_name = validated_token.get('role_name')
            if not user_id or not role_name:
                return None, None
            return user_id, role_name

        except (InvalidToken, TokenError, IndexError):
            return None, None

    def delete(self, request, order_product_id, *args, **kwargs):
        """
        Deletes a product entry in the order_table_product and updates the placeorder status if all products are deleted.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Check if the product entry exists in order_table_product
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT order_id FROM order_table_product WHERE order_product_id = %s", [order_product_id]
                )
                product_entry = cursor.fetchone()
            
            if not product_entry:
                return JsonResponse(
                    {"error": "Product entry not found in order_table_product."},
                    status=404
                )

            order_id = product_entry[0]

            # Delete the product entry from order_table_product
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM order_table_product WHERE order_product_id = %s", [order_product_id]
                )

            # Check if there are any remaining products for this order_id
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM order_table_product WHERE order_id = %s", [order_id]
                )
                remaining_count = cursor.fetchone()[0]

            if remaining_count == 0:
                # If no products left, update the status in the placeorder table
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE placeorder SET status = 'D' WHERE stockiest_order_id = %s", [order_id]
                    )

            return JsonResponse(
                {"message": "Product entry deleted from order_table_product. PlaceOrder status updated"},
                status=200
            )

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
