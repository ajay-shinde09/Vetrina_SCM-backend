from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime


class GetPendingOrders(View):
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

    def get(self, request, *args, **kwargs):
        """
        Retrieves details of orders where is_placed_order is 'P' for the current logged-in user.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Query to get orders with is_placed_order = 'P' for the logged-in user
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.name AS customer_name, 
                           cr.role_name AS customer_role, 
                           po.stockiest_order_id AS order_id,
                           po.created_date, 
                           po.status                           
                    FROM placeorder po
                    JOIN customer c ON po.user_id = c.customer_id
                    JOIN customer_roles cr ON c.role = cr.cust_role_id
                    WHERE po.status = 'P' AND po.user_id = %s
                """, [user_id])  # Filtering orders for the logged-in user

                results = cursor.fetchall()

            # Format results into a dictionary
            formatted_results = []
            for row in results:
                # Format order_date to show only the date
                order_date = row[3]
                if isinstance(order_date, datetime):
                    formatted_order_date = order_date.strftime('%Y-%m-%d')
                else:
                    formatted_order_date = order_date

                formatted_results.append({
                    "customer_name": row[0],
                    "customer_role": row[1],
                    "order_id": row[2],
                    "order_date": formatted_order_date,
                    "status": row[4]
                })

            return JsonResponse(formatted_results, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)



class InprocessOrders(View):
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

    def get(self, request, *args, **kwargs):
        """
        Retrieves details of orders where is_placed_order is 'P'.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Query to get orders with is_placed_order = 'P'
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.name AS customer_name, 
                           cr.role_name AS customer_role, 
                           po.stockiest_order_id AS order_id,
                           po.created_date, 
                           po.status                           
                    FROM placeorder po
                    JOIN customer c ON po.user_id = c.customer_id
                    JOIN customer_roles cr ON c.role = cr.cust_role_id
                    WHERE po.status = 'I' AND po.user_id = %s
                """, [user_id])  # Filtering orders for the logged-in user 

                results = cursor.fetchall()

            # Format results into a dictionary
            formatted_results = []
            for row in results:
                # Format order_date to show only the date
                order_date = row[3]
                if isinstance(order_date, datetime):
                    formatted_order_date = order_date.strftime('%Y-%m-%d')
                else:
                    formatted_order_date = order_date

                # Check dispatch_date and set "not dispatched" if null
              #  dispatch_date = row[4] if row[4] else "not dispatched"

                formatted_results.append({
                    "customer_name": row[0],
                    "customer_role": row[1],
                    "order_id":row[2],
                    "order_date": formatted_order_date,
                    "status": row[4]
                    #"dispatch_date": dispatch_date,
                })

            return JsonResponse(formatted_results, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)


class DispatchOrders(View):
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

    def get(self, request, *args, **kwargs):
        """
        Retrieves details of orders where is_placed_order is 'P'.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Query to get orders with is_placed_order = 'P'
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.name AS customer_name, 
                           cr.role_name AS customer_role, 
                           lr.dispatch_date,   
                           po.stockiest_order_id AS order_id,
                           po.created_date, 
                           po.status                            
                    FROM placeorder po
                    JOIN customer c ON po.user_id = c.customer_id
                    JOIN customer_roles cr ON c.role = cr.cust_role_id
                    JOIN lr_details lr ON po.stockiest_order_id = lr.order_id
                    WHERE po.status = 'Y'AND po.user_id = %s
                """, [user_id])  # Filtering orders for the logged-in user
                
                results = cursor.fetchall()

            # Format results into a dictionary
            formatted_results = []
            for row in results:
                # Format order_date to show only the date
                order_date = row[4]
                if isinstance(order_date, datetime):
                    formatted_order_date = order_date.strftime('%Y-%m-%d')
                else:
                    formatted_order_date = order_date


                dispatch_date = row[2]
                if isinstance(dispatch_date, datetime):
                    formatted_dispatch_date = dispatch_date.strftime('%Y-%m-%d')
                else:
                    formatted_dispatch_date = dispatch_date

                # Check dispatch_date and set "not dispatched" if null
              #  dispatch_date = row[4] if row[4] else "not dispatched"

                formatted_results.append({
                    "customer_name": row[0],
                    "customer_role": row[1],
                    "dispatch_date": formatted_dispatch_date,
                    "order_id": row[3],
                    "order_date": formatted_order_date,
                    "status": row[5]
                })

            return JsonResponse(formatted_results, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)



class DeliveredOrders(View):
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

    def get(self, request, *args, **kwargs):
        """
        Retrieves details of orders where is_placed_order is 'P'.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Query to get orders with is_placed_order = 'P'
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.name AS customer_name, 
                           cr.role_name AS customer_role, 
                           lr.dispatch_date,   
                           po.stockiest_order_id AS order_id,
                           po.created_date, 
                           po.status                            
                    FROM placeorder po
                    JOIN customer c ON po.user_id = c.customer_id
                    JOIN customer_roles cr ON c.role = cr.cust_role_id
                    JOIN lr_details lr ON po.stockiest_order_id = lr.order_id
                    WHERE po.status = 'D' AND po.user_id = %s
                """, [user_id])  # Filtering orders for the logged-in user
                
                results = cursor.fetchall()

            # Format results into a dictionary
            formatted_results = []
            for row in results:
                # Format order_date to show only the date
                order_date = row[4]
                if isinstance(order_date, datetime):
                    formatted_order_date = order_date.strftime('%Y-%m-%d')
                else:
                    formatted_order_date = order_date


                dispatch_date = row[2]
                if isinstance(dispatch_date, datetime):
                    formatted_dispatch_date = dispatch_date.strftime('%Y-%m-%d')
                else:
                    formatted_dispatch_date = dispatch_date

                # Check dispatch_date and set "not dispatched" if null
              #  dispatch_date = row[4] if row[4] else "not dispatched"

                formatted_results.append({
                    "customer_name": row[0],
                    "customer_role": row[1],
                    "dispatch_date": formatted_dispatch_date,
                    "order_id": row[3],
                    "order_date": formatted_order_date,
                    "status": row[5]
                })

            return JsonResponse(formatted_results, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

class CancelledOrders(View):
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

    def get(self, request, *args, **kwargs):
        """
        Retrieves details of orders where is_placed_order is 'P'.
        """
        try:
            # Authenticate user
            user_id, role_name = self.get_user_from_token(request)
            if not user_id or not role_name:
                return JsonResponse({'error': 'Authentication failed. Invalid or missing token.'}, status=401)

            # Query to get orders with is_placed_order = 'P'
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT c.name AS customer_name, 
                           cr.role_name AS customer_role, 
                           po.stockiest_order_id AS order_id,
                           po.created_date, 
                           po.status                           
                    FROM placeorder po
                    JOIN customer c ON po.user_id = c.customer_id
                    JOIN customer_roles cr ON c.role = cr.cust_role_id
                    WHERE po.status = 'N' AND po.user_id = %s
                """, [user_id])  # Filtering orders for the logged-in user
                
                results = cursor.fetchall()

            # Format results into a dictionary
            formatted_results = []
            for row in results:
                # Format order_date to show only the date
                order_date = row[3]
                if isinstance(order_date, datetime):
                    formatted_order_date = order_date.strftime('%Y-%m-%d')
                else:
                    formatted_order_date = order_date

                # Check dispatch_date and set "not dispatched" if null
              #  dispatch_date = row[4] if row[4] else "not dispatched"

                formatted_results.append({
                    "customer_name": row[0],
                    "customer_role": row[1],
                    "order_id": row[2],
                    "order_date": formatted_order_date,
                    "status": row[4]
                    #"dispatch_date": dispatch_date,
                })

            return JsonResponse(formatted_results, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)
