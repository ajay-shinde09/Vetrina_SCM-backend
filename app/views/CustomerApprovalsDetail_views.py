import os
from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from app.models import Customer
from app.serializers.CustomerApprovalsDetail_serializers import CustomerApprovalDetailSerializer  # Import the updated serializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import IsFinanceManager,IsNonAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomerApprovalDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsFinanceManager,IsNonAdminUser]  
    def get(self, request, customer_id):
        query = '''
    SELECT 
        c.name AS firm_name, 
        c.customer_id, 
        dt.distributor_type, 
        COALESCE(hq.hq_name, '') AS headquarter, 
        d.division_name AS division, 
        c.kyc_status,
        cr.role_name,  -- Get role_name from customer_roles
        s.state_name
    FROM customer c
    LEFT JOIN customer_hq_div chq ON c.customer_id = chq.customer_id
    LEFT JOIN headquarters hq ON chq.hq_id = hq.hq_id
    LEFT JOIN divisions d ON chq.div_id = d.division_id  
    LEFT JOIN distributor_type dt ON c.type = dt.distributor_type_id
    LEFT JOIN customer_roles cr ON c.role = cr.cust_role_id
    LEFT JOIN state s ON c.state_id = s.state_id 
    WHERE c.customer_id = %s
'''

        with connection.cursor() as cursor:
            cursor.execute(query, [customer_id])
            result = cursor.fetchone()

        if result is None:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "firm_name": result[0],
            "customer_id": result[1],
            "distributor_type": result[2],
            "headquarter": result[3],
            "division": result[4],
            "kyc_status": result[5],
            "role_name": result[6]
        }

        # Fetching customer meta data
        customer_meta_query = '''
            SELECT cm.customer_meta_key, cm.customer_meta_value, cr.role_name, s.state_name, dt.distributor_type,
            hq.hq_name, d.division_name, sup.sup_name
    FROM customer_meta cm
    JOIN customer c ON cm.customer_id = c.customer_id
    JOIN customer_roles cr ON c.role = cr.cust_role_id
    JOIN state s ON c.state_id = s.state_id
    JOIN distributor_type dt ON c.type = dt.distributor_type_id
    left JOIN customer_hq_div vhd ON c.customer_id = vhd.customer_id
    left JOIN headquarters hq ON vhd.hq_id = hq.hq_id
    left JOIN divisions d ON vhd.div_id = d.division_id
    left JOIN suppliers sup ON c.supplier = sup.supplier_id
    WHERE cm.customer_id = %s
        '''
        
        with connection.cursor() as cursor:
            cursor.execute(customer_meta_query, [customer_id])
            meta_results = cursor.fetchall()
        meta_data = {key: value for key, value,  _, _, _, _, _, _ in meta_results}
        role_name = meta_results[0][2] if meta_results else ''
        state_name=meta_results[0][3] if meta_results else ''
        stockiest_type=meta_results[0][4] if meta_results else ''
        hq_name = meta_results[0][5] if meta_results else ''
        division_name = meta_results[0][6] if meta_results else ''
        sup_name = meta_results[0][7] if meta_results else ''



        # Add relevant meta data to the main data dictionary
        data.update({
    "customer_id": meta_data.get('customer_id', ''),
    "cust_name": meta_data.get('cust_name', ''),
    "email": meta_data.get('email', ''),
    # "cust_role": meta_data.get('cust_role', ''),  # Added customer role
    "cust_role": role_name, 
    #"stockiest_type": meta_data.get('stockiest_type', ''),
    "stockiest_type": stockiest_type,
    "addressl1": meta_data.get('addressl1', ''),
    "addressl2": meta_data.get('addressl2', ''),
    "hq": hq_name,
    "division": division_name,
    "subDivision": meta_data.get('subDivision', ''),
    "vsoname": meta_data.get('vsoname', ''),
    "vsomob": meta_data.get('vsomob', ''),
    "taluka": meta_data.get('taluka', ''),
    "District": meta_data.get('District', ''),
    #"State": meta_data.get('State', ''), 
    "State":state_name,
    "Pin_code": meta_data.get('Pin_code', ''),
    "mob_no": meta_data.get('mob_no', ''),
    "geo_tag": meta_data.get('geo_tag', ''),
    "date_of_establishment": meta_data.get('date_of_establishment', ''),
    "gst_no": meta_data.get('gst_no', ''),
    "pan_no": meta_data.get('pan_no', ''),
    "drug_licence_no": meta_data.get('drug_licence_no', ''),
    "from_date": meta_data.get('from_date', ''),
    "to_date": meta_data.get('to_date', ''),
    "bank_name": meta_data.get('bank_name', ''),
    "bank_ac_no": meta_data.get('bank_ac_no', ''),
    "bank_ifsc": meta_data.get('bank_ifsc', ''),
    "bank_address": meta_data.get('bank_address', ''),
    "anual_turnover": meta_data.get('anual_turnover', ''),
    "no_of_company": meta_data.get('no_of_company', ''),
    "area_state": meta_data.get('area_state', ''),
    "area_district": meta_data.get('area_district', ''),
    "expected_anual_business": meta_data.get('expected_anual_business', ''),
    "contact_person_name": meta_data.get('contact_person_name', ''),
    "contact_person_mobile": meta_data.get('contact_person_mobile', ''),
    "contact_person_email": meta_data.get('contact_person_email', ''),
    "supplier": sup_name,  # Added supplier
    "cnf": meta_data.get('cnf', ''),  # Added CNF
    "update_customer": meta_data.get('update_customer', '') , # Added update customer field
    "credit_days": meta_data.get('credit_days', None),
    "credit_limit": meta_data.get('credit_limit', None)
})
        kyc_documents_query = '''
            SELECT cust_kyc_id, document
            FROM customer_kyc_document
            WHERE customer_id = %s
        '''

        with connection.cursor() as cursor:
            cursor.execute(kyc_documents_query, [customer_id])
            kyc_documents = cursor.fetchall()

        kyc_documents_list = []
        for idx, doc in enumerate(kyc_documents, start=1):  # Using enumerate for SR No.
            file_path = doc[1]  # Full path of the document in the database
            file_name = os.path.basename(file_path)  # Extract the file name from the path

            # Append extension if missing, based on keywords in the filename
            if not file_name.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif')):
                if 'pdf' in file_name.lower():
                    file_name += '.pdf'
                elif 'jpg' in file_name.lower() or 'jpeg' in file_name.lower():
                    file_name += '.jpg'
                elif 'png' in file_name.lower():
                    file_name += '.png'
                elif 'gif' in file_name.lower():
                    file_name += '.gif'

            document_url = f"{settings.MEDIA_URL}customer_kyc_document/{file_name}"
            
            # Modify the image URL to remove the '.pdf' extension if the file is a PDF
            if file_name.endswith('.pdf'):
                # For PDF files, use the same base name but change the extension to '.jpg'
                file_img = f"{settings.MEDIA_URL}customer_kyc_document/{file_name.replace('.pdf', '.jpg')}"
            elif file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # For image files, use the same file as the view image
                file_img = document_url
            else:
                # For other file types, use a default image
                file_img = f"{settings.MEDIA_URL}customer_kyc_document/{file_name}.jpg"

            kyc_documents_list.append({
                'sr_no': idx,               # SR No. starts from 1
                'file_name': file_name,      # File name with correct extension
                'view_file_img': file_img,   # Full URL to the image (or PDF icon) for preview
                'view_file': document_url,   # Full URL for viewing/downloading the file
            })

        data['kyc_documents'] = kyc_documents_list

        serializer = CustomerApprovalDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, customer_id):
        try:
            # Fetch data from request
            credit_limit = request.data.get('credit_limit')
            credit_days = request.data.get('credit_days')

            with connection.cursor() as cursor:
                # Update customer_meta fields for credit_limit and credit_days
                cursor.execute("""
                    INSERT INTO customer_meta (customer_id, customer_meta_key, customer_meta_value)
                    VALUES 
                        (%s, 'credit_limit', %s),
                        (%s, 'credit_days', %s)
                    ON DUPLICATE KEY UPDATE
                    customer_meta_value = CASE customer_meta_key 
                        WHEN 'credit_limit' THEN %s
                        WHEN 'credit_days' THEN %s
                    END
                """, [customer_id, credit_limit, customer_id, credit_days, credit_limit, credit_days])

#AND customer_meta_key IN ('credit_limit', 'credit_days')
                # Update approval_status in the customer table to 'F' (approved)
                cursor.execute("""
                    UPDATE customer
                    SET approval_status = 'F'
                    WHERE customer_id = %s
                """, [customer_id])

                # Insert into credit_note_user_detail table
                cursor.execute("""
                    INSERT INTO credit_note_user_details (user_id, credit_limit, credit_days)
                    VALUES (%s, %s, %s)
                """, [customer_id, credit_limit, credit_days])


            return Response({'status': 'success', 'message': 'Customer approved and updated'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)