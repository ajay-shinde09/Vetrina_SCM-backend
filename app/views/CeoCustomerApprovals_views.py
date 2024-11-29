from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework import status
from django.urls import reverse
from app.serializers.CeoCustomerApprovals_serializers import CeoCustomerApprovalListSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsChiefExecutiveOfficer,IsNonAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class CeoCustomerApprovalListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsChiefExecutiveOfficer,IsNonAdminUser]  

    def get(self, request):
        with connection.cursor() as cursor:
            query = '''
                SELECT
                    c.customer_id,
                    c.name AS firm_name,
                    cr.role_name AS role,
                    dt.distributor_type AS type,
                    c.email,
                    c.mobile_number,
                    c.created_on AS registration_date,
                    c.approval_status
                FROM
                    customer c
                JOIN
                    customer_roles cr ON c.role = cr.cust_role_id
                JOIN
                    distributor_type dt ON c.type = dt.distributor_type_id
                WHERE
                    c.approval_status = 'F'
            '''
            cursor.execute(query)
            results = cursor.fetchall()

            # Creating a list of dictionaries for serializer
            columns = ['customer_id', 'firm_name', 'role', 'type', 'email', 'mobile_number', 'registration_date', 'approval_status']
            data = [dict(zip(columns, row)) for row in results]

            # Add 'sr_no' using Python (index + 1)
            for indx, customer in enumerate(data, start=1):
                customer['sr_no'] = indx

                # Add action link
                customer['action_link'] = reverse('Ceo_customers_approval_detail', args=[customer['customer_id']])


            # Use the serializer with `data`
            serializer = CeoCustomerApprovalListSerializer(data, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
