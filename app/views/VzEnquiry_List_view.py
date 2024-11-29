from rest_framework import generics
from rest_framework.response import Response
from app.models import Vetzone
from app.serializers.VzEnquiry_List_serializers import VetzoneEnquirySerializer,VetzoneEnquiryDetailSerializer
from django.conf import settings
import os
from rest_framework import status
from django.db import connection, transaction

class VetzoneEnquiryListView(generics.ListAPIView):
    serializer_class = VetzoneEnquirySerializer

    def get_queryset(self):
        return Vetzone.objects.filter(approval_status='N')

    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Calculate counts
        new_enquiries = Vetzone.objects.filter(approval_status='N').count()
        approved_requests = Vetzone.objects.filter(approval_status='N').count()
        pending_establishments = Vetzone.objects.filter(establishment_status='N').count()
        established = Vetzone.objects.filter(establishment_status='Y').count()

        response_data = {
            'counts': {
                'new_enquiries': new_enquiries,
                'approved_requests': approved_requests,
                'pending_establishments': pending_establishments,
                'established': established,
            },
            'enquiries': serializer.data
        }

        return Response(response_data)

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import os
class VetzoneEnquiryDetailView(APIView):

        def get(self,request, vetzone_id):
            with connection.cursor() as cursor:
                cursor.execute(""" 
                    SELECT   
        v.vetzone_id, 
        vt.v_type_name AS type, 
        hq.hq_name AS headquarter, 
        d.division_name AS division,
        v.geo_location,  -- Vetzone geo_location
        v.approval_status AS status
    FROM 
        vetzone v
    LEFT JOIN 
        vetzone_type vt ON v.type = vt.v_type_id
    LEFT JOIN 
        vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id
    LEFT JOIN 
        headquarters hq ON vhd.hq_id = hq.hq_id
    LEFT JOIN 
        divisions d ON vhd.div_id = d.division_id
    WHERE 
        v.vetzone_id = %s;

                """, [vetzone_id])
                result = cursor.fetchone()

            if not result:
                return Response({"error": "Vetzone not found"}, status=404)

            # Query to get additional details from vetzone_meta, including state_name from the state table
            with connection.cursor() as cursor:
                cursor.execute(""" 
                    SELECT 
                v.vetzone_id, 
                v.owner_name, 
                vm_email.vetzone_meta_value AS email, 
                vm_address1.vetzone_meta_value AS address_l1, 
                vm_address2.vetzone_meta_value AS address_l2, 
                vm_village.vetzone_meta_value AS village,
                vm_taluka.vetzone_meta_value AS taluka, 
                vm_district.vetzone_meta_value AS district, 
                s.state_name AS state,  
                vm_pincode.vetzone_meta_value AS pincode, 
                vm_mobile.vetzone_meta_value AS mobile_number, 
                vm_total_milk.vetzone_meta_value AS total_milk_collection, 
                vm_total_mcc.vetzone_meta_value AS total_number_MCC,
                v.name AS vetzone_name,
                vm_est_date.vetzone_meta_value AS establishment_date,
                vm_vetzone_addr.vetzone_meta_value AS vetzone_address,
                vm_ifsc.vetzone_meta_value AS ifsc_code,
                vm_ac_number.vetzone_meta_value AS ac_number,
                vm_ac_holder_name.vetzone_meta_value AS ac_holder_name,
                vm_bank_name.vetzone_meta_value AS bank_name,
                vm_alt_contact.vetzone_meta_value AS alternate_contact_number,  -- Add alternate contact number
                a.username AS vso_name,  -- Get VSO Name
                am.mob_number_company AS vso_mobile
            FROM vetzone v
            LEFT JOIN vetzone_meta vm_email ON v.vetzone_id = vm_email.vetzone_id 
                AND vm_email.vetzone_meta_key = 'email'
            LEFT JOIN vetzone_meta vm_address1 ON v.vetzone_id = vm_address1.vetzone_id 
                AND vm_address1.vetzone_meta_key = 'addressl1'
            LEFT JOIN vetzone_meta vm_address2 ON v.vetzone_id = vm_address2.vetzone_id 
                AND vm_address2.vetzone_meta_key = 'addressl2'
            LEFT JOIN vetzone_meta vm_village ON v.vetzone_id = vm_village.vetzone_id 
                AND vm_village.vetzone_meta_key = 'Village'
            LEFT JOIN vetzone_meta vm_taluka ON v.vetzone_id = vm_taluka.vetzone_id 
                AND vm_taluka.vetzone_meta_key = 'taluka'
            LEFT JOIN vetzone_meta vm_district ON v.vetzone_id = vm_district.vetzone_id 
                AND vm_district.vetzone_meta_key = 'District'
            LEFT JOIN vetzone_meta vm_state ON v.vetzone_id = vm_state.vetzone_id 
                AND vm_state.vetzone_meta_key = 'State'
            LEFT JOIN state s ON vm_state.vetzone_meta_value = s.state_id  
            LEFT JOIN vetzone_meta vm_pincode ON v.vetzone_id = vm_pincode.vetzone_id 
                AND vm_pincode.vetzone_meta_key = 'Pin_code'
            LEFT JOIN vetzone_meta vm_mobile ON v.vetzone_id = vm_mobile.vetzone_id 
                AND vm_mobile.vetzone_meta_key = 'mob_no'
            LEFT JOIN vetzone_meta vm_total_milk ON v.vetzone_id = vm_total_milk.vetzone_id 
                AND vm_total_milk.vetzone_meta_key = 'total_milk_collection'
            LEFT JOIN vetzone_meta vm_total_mcc ON v.vetzone_id = vm_total_mcc.vetzone_id 
                AND vm_total_mcc.vetzone_meta_key = 'total_number_MCC'
            LEFT JOIN vetzone_meta vm_est_date ON v.vetzone_id = vm_est_date.vetzone_id
                AND vm_est_date.vetzone_meta_key = 'establishment_date'
            LEFT JOIN vetzone_meta vm_vetzone_addr ON v.vetzone_id = vm_vetzone_addr.vetzone_id
                AND vm_vetzone_addr.vetzone_meta_key = 'vetzone_address'
            LEFT JOIN vetzone_meta vm_ifsc ON v.vetzone_id = vm_ifsc.vetzone_id
                AND vm_ifsc.vetzone_meta_key = 'ifsc'
            LEFT JOIN vetzone_meta vm_ac_number ON v.vetzone_id = vm_ac_number.vetzone_id
                AND vm_ac_number.vetzone_meta_key = 'ac_number'
            LEFT JOIN vetzone_meta vm_ac_holder_name ON v.vetzone_id = vm_ac_holder_name.vetzone_id
                AND vm_ac_holder_name.vetzone_meta_key = 'ac_holder_name'
            LEFT JOIN vetzone_meta vm_bank_name ON v.vetzone_id = vm_bank_name.vetzone_id
                AND vm_bank_name.vetzone_meta_key = 'bank_name'
            LEFT JOIN vetzone_meta vm_alt_contact ON v.vetzone_id = vm_alt_contact.vetzone_id
                AND vm_alt_contact.vetzone_meta_key = 'alternate_contact_number'  -- Join for alternate contact number
            INNER JOIN 
        vetzone_hq_div vhd ON v.vetzone_id = vhd.vetzone_id  -- Join vetzone_hq_div for HQ and division info
    INNER JOIN 
        headquarters hq ON vhd.hq_id = hq.hq_id  -- Join HQ info
    INNER JOIN 
        divisions d ON vhd.div_id = d.division_id  -- Join division info
    INNER JOIN 
        admin_hq_div ahd ON vhd.hq_id = ahd.hq_id  -- Join admin_hq_div to match HQ and division
    INNER JOIN 
        admin a ON ahd.admin_id = a.admin_id  -- Get admin details (VSO name)
    INNER JOIN 
        admin_meta am ON a.admin_id = am.admin_id  -- Get admin's mobile number
            WHERE v.vetzone_id = %s;
                """, [vetzone_id])
                result1 = cursor.fetchone()

            if not result1:
                return Response({"error": "Vetzone details not found"}, status=404)

            # Query to get KYC documents for the Vetzone
            with connection.cursor() as cursor:
                cursor.execute(""" 
                    SELECT 
                        vetzone_kyc_id, 
                        document, 
                        approval_status, 
                        uploaded_on
                    FROM 
                        vetzone_kyc_document
                    WHERE 
                        vetzone_id = %s;
                """, [vetzone_id])
                kyc_docs = cursor.fetchall()

            # Construct KYC documents data
            kyc_documents = []
            for idx, doc in enumerate(kyc_docs, start=1):
                file_url = os.path.join(settings.MEDIA_URL, 'vetzone_kyc_document', doc[1]) if doc[1] else None
                kyc_documents.append({
                    "Sr No": idx,
                    "File Name": doc[1],
                    "View File IMG": file_url,
                    "View File": file_url,
                })
        
            # Construct the main response data
            data = {
                "vetzone_id": result[0],
        "Type": result[1] if result[1] else "",
        "Headquarter": result[2] if result[2] else "",
        "Division": result[3] if result[3] else "",
        "Status":result[5] if result[5] else "",  
        "Details": {
            "VetZone ID": result1[0],
            "Name of Owner": result1[1],
            "Email": result1[2] if result1[2] else "",
            "Address l1": result1[3] if result1[3] else "",
            "Address l2": result1[4] if result1[4] else "",
            "Village": result1[5] if result1[5] else "",
            "Taluka": result1[6] if result1[6] else "",
            "District": result1[7] if result1[7] else "",
            "State": result1[8] if result1[8] else "",
            "Pincode": result1[9] if result1[9] else "",
            "Mobile Number": result1[10] if result1[10] else "",
            "Total Milk Collection": result1[11] if result1[11] else "",
            "Total Number of MCC": result1[12] if result1[12] else "",
            "Headquarter": result[2] if result[2] else "",
            "Division": result[3] if result[3] else "",
            "VSO Name": result1[21] if result1[21] else "" ,  
            "VSO Mobile Number": result1[22] if result1[22] else "" , 
            "Type": result[1] if result[1] else "",
            "Name of VetZone": result1[13] if result1[13] else "",
            "Establishment Date": result1[14] if result1[14] else "",
            "VetZone Address": result1[15] if result1[15] else "",
            "IFSC Code": result1[16] if result1[16] else "",
            "Account Number": result1[17] if result1[17] else "",
            "Account Holder Name": result1[18] if result1[18] else "",
            "Bank Name": result1[19] if result1[19] else "",
            "Geo Location": result[4] if result[4] else "",
            "Alternate Contact Number": result1[20] if result1[20] else "",  # Alternate Contact Number
            "KYC Documents": kyc_documents
                }
            }
            
            return Response(data)
        
        @transaction.atomic
        def put(self, request, vetzone_id):
            try:
        # Fetch the Vetzone instance to update
                try:
                    vetzone = Vetzone.objects.get(vetzone_id=vetzone_id)
                except Vetzone.DoesNotExist:
                    return Response({"error": "Vetzone not found"}, status=404)

        # Use the serializer to validate and update the Vetzone model
                serializer = VetzoneEnquiryDetailSerializer(vetzone, data=request.data)
                if serializer.is_valid():
                    serializer.save()
            # Validate the input data
                    data = request.data

            # Extract fields from the request data
                    vetzone_id = data.get('vetzone_id')
                    owner_name = data.get('owner_name')
                    email = data.get('email')
                    address_l1 = data.get('address_l1')
                    address_l2 = data.get('address_l2')
                    village = data.get('village')
                    taluka = data.get('taluka')
                    district = data.get('district')
                    pincode = data.get('pincode')
                    mobile_number = data.get('mobile_number')
                    total_milk_collection = data.get('total_milk_collection')
                    total_number_mcc = data.get('total_number_mcc')
                    vetzone_name = data.get('vetzone_name')
                    establishment_date = data.get('establishment_date')
                    vetzone_address = data.get('vetzone_address')
                    ifsc_code = data.get('ifsc_code')
                    ac_number = data.get('ac_number')
                    ac_holder_name = data.get('ac_holder_name')
                    bank_name = data.get('bank_name')
                    alt_contact = data.get('alternate_contact_number')
                    vso_name = data.get('username')
                    vso_mobile = data.get('mob_number_company')
                    headquarters = data.get('headquarters')
                    division = data.get('division')
                    vetzone_type = data.get('type')
                    state = data.get('state')

            # Update main `vetzone` table
                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE vetzone
                            SET owner_name = %s, geo_location = %s, name = %s,headquarters = %s, division = %s, type = %s, state = %s
                            WHERE vetzone_id = %s;
                        """, [owner_name, data.get('geo_location'), vetzone_name, headquarters, division, vetzone_type, state,vetzone_id])

            # Update `vetzone_meta` data
                    with connection.cursor() as cursor:
                        # Update email
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'email';
                        """, [email, vetzone_id])

                        # Update address line 1
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'addressl1';
                        """, [address_l1, vetzone_id])

                        # Update address line 2
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'addressl2';
                        """, [address_l2, vetzone_id])

                        # Update village
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'Village';
                        """, [village, vetzone_id])

                        # Update taluka
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'taluka';
                        """, [taluka, vetzone_id])

                        # Update district
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'District';
                        """, [district, vetzone_id])

                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'headquarters';
                        """, [headquarters, vetzone_id])

                # Update division
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'division';
                        """, [division, vetzone_id])

                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'type';
                        """, [type, vetzone_id])

                # Update division
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'state';
                        """, [state, vetzone_id])

                        # Update pincode
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'Pin_code';
                        """, [pincode, vetzone_id])

                        # Update mobile number
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'mob_no';
                        """, [mobile_number, vetzone_id])

                        # Update total milk collection
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'total_milk_collection';
                        """, [total_milk_collection, vetzone_id])

                        # Update total MCC
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'total_number_MCC';
                        """, [total_number_mcc, vetzone_id])

                        # Update establishment date
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'establishment_date';
                        """, [establishment_date, vetzone_id])

                        # Update vetzone address
                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'vetzone_address';
                        """, [vetzone_address, vetzone_id])

                        cursor.execute("""
                            UPDATE vetzone_meta 
                            SET vetzone_meta_value = %s 
                            WHERE vetzone_id = %s AND vetzone_meta_key = 'alternate_contact_number';
                        """, [alt_contact, vetzone_id])

                    # Update VSO name in admin
                    cursor.execute("""
                        UPDATE admin 
                        SET username = %s 
                        WHERE admin_id = (SELECT admin_id FROM admin_hq_div WHERE hq_id = (SELECT hq_id FROM vetzone_hq_div WHERE vetzone_id = %s));
                    """, [vso_name, vetzone_id])

                    # Update VSO mobile number in admin_meta
                    cursor.execute("""
                        UPDATE admin_meta 
                        SET mob_number_company = %s 
                        WHERE admin_id = (SELECT admin_id FROM admin_hq_div WHERE hq_id = (SELECT hq_id FROM vetzone_hq_div WHERE vetzone_id = %s));
                    """, [vso_mobile, vetzone_id])

                    # Update headquarters in vetzone_hq_div
                    cursor.execute("""
                        UPDATE vetzone_hq_div 
                        SET hq_id = (SELECT hq_id FROM headquarters WHERE hq_name = %s) 
                        WHERE vetzone_id = %s;
                    """, [headquarters, vetzone_id])

                    # Update division in vetzone_hq_div
                    cursor.execute("""
                        UPDATE vetzone_hq_div 
                        SET div_id = (SELECT division_id FROM divisions WHERE division_name = %s) 
                        WHERE vetzone_id = %s;
                    """, [division, vetzone_id])

                    # Update vetzone type
                    cursor.execute("""
                        UPDATE vetzone 
                        SET type = (SELECT v_type_id FROM vetzone_type WHERE v_type_name = %s) 
                        WHERE vetzone_id = %s;
                    """, [vetzone_type, vetzone_id])

                    # Update state in vetzone_meta
                    cursor.execute("""
                        UPDATE vetzone_meta 
                        SET vetzone_meta_value = (SELECT state_id FROM state WHERE state_name = %s) 
                        WHERE vetzone_id = %s AND vetzone_meta_key = 'State';
                    """, [state, vetzone_id])


                    with connection.cursor() as cursor:
                        # Check if the keys exist in vetzone_meta for the given vetzone_id
                        cursor.execute("""
                            SELECT vetzone_meta_key 
                            FROM vetzone_meta 
                            WHERE vetzone_id = %s AND vetzone_meta_key IN ('ifsc_code', 'ac_number', 'ac_holder_name', 'bank_name')
                        """, [vetzone_id])

                        existing_meta_keys = [row[0] for row in cursor.fetchall()]

                        # Insert missing keys
                        if 'ifsc_code' not in existing_meta_keys and ifsc_code:
                            cursor.execute("""
                                INSERT INTO vetzone_meta (vetzone_id, vetzone_meta_key, vetzone_meta_value)
                                VALUES (%s, 'ifsc_code', %s)
                            """, [vetzone_id, ifsc_code])

                        if 'ac_number' not in existing_meta_keys and ac_number:
                            cursor.execute("""
                                INSERT INTO vetzone_meta (vetzone_id, vetzone_meta_key, vetzone_meta_value)
                                VALUES (%s, 'ac_number', %s)
                            """, [vetzone_id, ac_number])

                        if 'ac_holder_name' not in existing_meta_keys and ac_holder_name:
                            cursor.execute("""
                                INSERT INTO vetzone_meta (vetzone_id, vetzone_meta_key, vetzone_meta_value)
                                VALUES (%s, 'ac_holder_name', %s)
                            """, [vetzone_id, ac_holder_name])

                        if 'bank_name' not in existing_meta_keys and bank_name:
                            cursor.execute("""
                                INSERT INTO vetzone_meta (vetzone_id, vetzone_meta_key, vetzone_meta_value)
                                VALUES (%s, 'bank_name', %s)
                            """, [vetzone_id, bank_name])

                        # Update existing meta keys
                        if 'ifsc_code' in existing_meta_keys and ifsc_code:
                            cursor.execute("""
                                UPDATE vetzone_meta 
                                SET vetzone_meta_value = %s 
                                WHERE vetzone_id = %s AND vetzone_meta_key = 'ifsc_code'
                            """, [ifsc_code, vetzone_id])

                        if 'ac_number' in existing_meta_keys and ac_number:
                            cursor.execute("""
                                UPDATE vetzone_meta 
                                SET vetzone_meta_value = %s 
                                WHERE vetzone_id = %s AND vetzone_meta_key = 'ac_number'
                            """, [ac_number, vetzone_id])

                        if 'ac_holder_name' in existing_meta_keys and ac_holder_name:
                            cursor.execute("""
                                UPDATE vetzone_meta 
                                SET vetzone_meta_value = %s 
                                WHERE vetzone_id = %s AND vetzone_meta_key = 'ac_holder_name'
                            """, [ac_holder_name, vetzone_id])

                        if 'bank_name' in existing_meta_keys and bank_name:
                            cursor.execute("""
                                UPDATE vetzone_meta 
                                SET vetzone_meta_value = %s 
                                WHERE vetzone_id = %s AND vetzone_meta_key = 'bank_name'
                            """, [bank_name, vetzone_id])


                # If everything is successful, return a success response
                return Response({"message": "Vetzone details updated successfully"}, status=status.HTTP_200_OK)

            except Exception as e:
                # If there's an error, return it
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)