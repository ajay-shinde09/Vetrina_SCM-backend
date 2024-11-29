from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import quote
from django.conf import settings
import json

class LRVerificationAPI(View):
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

    def put(self, request, *args, **kwargs):
        """
        Verifies the LR number for the given order_id and changes the order status to 'Y' if verified.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Parse JSON body from request
            try:
                body = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format.'}, status=400)

            # Get the lrno and order_id from the request body
            lrno = body.get('lrno')
            order_id = body.get('order_id')

            if not lrno or not order_id:
                return JsonResponse({'error': "'lrno' and 'order_id' are required."}, status=400)

            # Fetch the existing LR number and its verification status from the database
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT lrno, file, is_verified
                    FROM lr_details
                    WHERE order_id = %s;
                """, [order_id])
                result = cursor.fetchone()

                if not result:
                    return JsonResponse({'error': 'Order ID not found.'}, status=404)

                existing_lrno, file_path, is_verified = result

                # Verify that the entered LR number matches the existing one
                if existing_lrno != lrno:
                    return JsonResponse({'error': 'LR number does not match the existing one.'}, status=400)

                # If the LR number is already verified, return a message
                if is_verified == 'Y':
                    return JsonResponse({'message': 'LR number is already verified.'}, status=200)

                # Update the LR verification status to 'Y'
                cursor.execute("""
                    UPDATE lr_details
                    SET is_verified = 'Y'
                    WHERE order_id = %s;
                """, [order_id])

                # Construct the full file URL if a file path exists
                receipt_image_url = None
                if file_path:
                    sanitized_path = file_path.replace('\\', '/')
                    encoded_path = quote(sanitized_path)
                    receipt_image_url = f"{settings.MEDIA_URL}lr_files/{encoded_path}"

                # Return success message along with the receipt image URL
                return JsonResponse({
                    'message': 'LR number verified and status updated successfully.',
                    'receipt_image_url': receipt_image_url
                }, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
