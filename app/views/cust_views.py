from django.utils import timezone
import os
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from app.serializers.cust_serializers import (
    CandFSerializer, DoctorSerializer, FarmerSerializer, KeyAccountSerializer, LSSSerializer, PetOwnerSerializer,
    PetshopSerializer, RetailerSerializer, StockiestSerializer, VetZoneSerializer
)
from app.models import Customer, CustomerHqDiv, CustomerKycDocument, CustomerMeta, Vetzone, VetzoneHqDiv, VetzoneMeta
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from django.core.exceptions import SuspiciousFileOperation
from rest_framework.permissions import AllowAny


class CustomerRegistrationnewView(APIView):
    permission_classes = [AllowAny]

    def validate_filename(filename):
        if '..' in filename or filename.startswith('/'):
            raise SuspiciousFileOperation("Invalid file path.")

    def post(self, request, *args, **kwargs):
        cust_role_id = request.data.get('cust_role_id')

        # Role-based serializer selection using a dictionary lookup
        role_serializers = {
            '1': CandFSerializer, '2': StockiestSerializer, '3': KeyAccountSerializer,
            '4': RetailerSerializer, '5': PetshopSerializer, '6': FarmerSerializer,
            '7': DoctorSerializer, '8': LSSSerializer , '9': PetOwnerSerializer,
            '10': VetZoneSerializer
        }

        serializer_class = role_serializers.get(cust_role_id)

        if not serializer_class:
            return Response({"error": "Invalid customer role ID"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            customer_data = serializer.validated_data
            password = request.data.get('password', '123456')
            hashed_password = make_password(password)

            vetzone = None
            customer = None

            try:

                if cust_role_id == '10':

                    vetzone = Vetzone.objects.create(
                        owner_name=serializer.validated_data.get('cust_name', ''),
                        email=serializer.validated_data.get('email', ''),
                        mobile_number=serializer.validated_data.get('mob_no', ''),
                        password=hashed_password,
                        type=serializer.validated_data.get('vetzone_type', 0),
                        role=cust_role_id,
                        kyc_status='N',
                        approval_status='N',
                        is_registered='N',
                        created_on=timezone.now(),
                        placeorder='N',
                        state_id=serializer.validated_data.get('State'),
                        establishment_status='N',
                        remark=serializer.validated_data.get('remark', '')
                    )

                    VetzoneHqDiv.objects.create(
                    vetzone_id=vetzone.vetzone_id,
                    hq_id=1,
                    div_id=1,
                    approval_admin_id=1,
                    sub_division=''
                    )

                    self.save_vetzone_meta(vetzone, customer_data)
                    message = "Vetzone registration successful"
                else:
    # Save data to Customer and related tables for other roles
                    customer = Customer.objects.create(
                        name=customer_data.get('firm_name', ''),
                        owner_name=customer_data.get('cust_name', ''),
                        mobile_number=customer_data.get('mob_no'),
                        email=customer_data.get('email'),
                        type=customer_data.get('type', '6'),  # Save the customer role as type
                        role=cust_role_id,
                        kyc_status='N',  # Default KYC status to Pending
                        approval_status='P',  # Default approval status to Pending
                        is_block='N',  # Default value for is_block
                        created_on=timezone.now(),
                        state_id=customer_data.get('State'),
                        terms_conditions='N' if request.data.get('terms_conditions', False) else 'Y',
                        supplier=None,
                        farmer_type=customer_data.get('farmer_type', None),
                        reference=customer_data.get('reference_from', None),
                        placeorder='Y',
                        password=hashed_password
                )

                self.save_customer_kyc_documents(customer, customer_data)
                self.save_customer_hq_div(customer)
                self.save_customer_meta(customer, customer_data, cust_role_id)
                message = "Customer registration successful"

                return Response({"message": message}, status=status.HTTP_201_CREATED)
            except Exception as e:
                            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save_customer_kyc_documents(self, customer, customer_data):
        if not customer:
            return

        kyc_documents = [
            ('address_proof', customer_data.get('address_proof')),
            ('firm_address_proof', customer_data.get('firm_address_proof')),
            ('pan_card', customer_data.get('pan_card')),
            ('aadhar_card', customer_data.get('aadhar_card')),
            ('gst_certificate', customer_data.get('gst_certificate')),
            ('cancelled_check', customer_data.get('cancelled_check')),
            ('photo', customer_data.get('photo')),
            ('drug_licence', customer_data.get('drug_licence')),
            ('msme_certificate', customer_data.get('msme_certificate')),
            ('registration_certificate', customer_data.get('registration_certificate')),
            ('clinic_address_proof', customer_data.get('clinic_address_proof')),
        ]

        for doc_key, doc_file in kyc_documents:
            if doc_file:
                # Create a new filename
                file_name, file_extension = os.path.splitext(doc_file.name)
                new_filename = f'{customer.customer_id}_{slugify(customer.owner_name)}_{slugify(file_name)}{file_extension}'
                relative_file_path = os.path.join('customer_kyc_document', new_filename)

                # Save the file in binary format
                default_storage.save(relative_file_path, ContentFile(doc_file.read()))

                # Save file metadata to the database
                CustomerKycDocument.objects.create(
                    customer_id=customer.customer_id,
                    document=new_filename,  # Save relative file path
                    approval_satatus='N',
                    uploaded_on=timezone.now(),
                )


    def save_customer_hq_div(self, customer):
        if not customer:
            return
        CustomerHqDiv.objects.create(
                customer_id=customer.customer_id,
                hq_id=1,
                div_id=1,
                approval_admin_id=1,
                sub_division=''
        )

    def save_customer_meta(self, customer, customer_data, cust_role_id):
        if not customer:
            return
        meta_data = {}
        if cust_role_id in ['2', '1', '3']:
                meta_data = {
                    'cust_role': cust_role_id,
                    'firm_name': customer_data.get('firm_name', ''),
                    'mob_no': customer_data.get('mob_no', ''),
                    'email': customer_data.get('email', ''),
                    'addressl1': customer_data.get('addressl1', ''),
                    'addressl2': customer_data.get('addressl2', ''),
                    'taluka': customer_data.get('taluka', ''),
                    'District': customer_data.get('District', ''),
                    'State': customer_data.get('State', ''),
                    'Pin_code': customer_data.get('Pin_code', ''),
                    'geo_tag': customer_data.get('geo_tag', ''),
                    'stockiest_type': customer_data.get('type', ''),
                    'cust_name': customer_data.get('cust_name', ''),
                    'date_of_establishment': customer_data.get('date_of_establishment', ''),
                    'gst_no': customer_data.get('gst_no', ''),
                    'pan_no': customer_data.get('pan_no', ''),
                    'drug_licence_no': customer_data.get('drug_licence_no', ''),
                    'anual_turnover': customer_data.get('anual_turnover', ''),
                    'no_of_company': customer_data.get('no_of_company', ''),
                    'area_state': customer_data.get('area_state', ''),
                    'area_district': customer_data.get('area_district', ''),
                    'from_date': customer_data.get('from_date', ''),
                    'to_date': customer_data.get('to_date', ''),
                    'bank_name': customer_data.get('bank_name', ''),
                    'bank_ac_no': customer_data.get('bank_ac_no', ''),
                    'bank_ifsc': customer_data.get('bank_ifsc', ''),
                    'bank_address': customer_data.get('bank_address', ''),
                    'expected_anual_business': customer_data.get('expected_anual_business', ''),
                    'contact_person_name': customer_data.get('contact_person_name', ''),
                    'contact_person_mobile': customer_data.get('contact_person_mobile', ''),
                    'contact_person_email': customer_data.get('contact_person_email', ''),
                }
        elif cust_role_id == '6':  # Other roles
                meta_data = {
                    'cust_role': cust_role_id,
                    'firm_name': customer_data.get('firm_name', ''),
                    'mob_no': customer_data.get('mob_no', ''),
                    'cust_name': customer_data.get('cust_name', ''),
                    'email': customer_data.get('email', ''),
                    'addressl1': customer_data.get('addressl1', ''),
                    'addressl2': customer_data.get('addressl2', ''),
                    'Pin_code': customer_data.get('Pin_code', ''),
                    'State': customer_data.get('State', ''),
                    'District': customer_data.get('District', ''),
                    'farmer_type': customer_data.get('farmer_type', ''),
                    'reference_from': customer_data.get('reference_from', ''),
                    'taluka':customer_data.get('taluka', ''),
                    'geo_tag':customer_data.get('geo_tag', ''),

                }
        elif cust_role_id in ['4', '5']:
                meta_data = {
                    'cust_role': cust_role_id,
                    'firm_name': customer_data.get('firm_name', ''),
                    'mob_no': customer_data.get('mob_no', ''),
                    'email': customer_data.get('email', ''),
                    'addressl1': customer_data.get('addressl1', ''),
                    'addressl2': customer_data.get('addressl2', ''),
                    'Pin_code': customer_data.get('Pin_code', ''),
                    'State': customer_data.get('State', ''),
                    'District': customer_data.get('District', ''),
                    'taluka': customer_data.get('Taluka', ''),
                    'geo_tag': customer_data.get('geo_tag', ''),
                    'gst_no': customer_data.get('gst_no', ''),
                    'drug_licence_no': customer_data.get('drug_licence_no', ''),
                    'anual_turnover': customer_data.get('anual_turnover', '')
                    }
        elif cust_role_id in ['7','8']:
                meta_data = {
                     'cust_role': cust_role_id,
                     'cust_name': customer_data.get('cust_name', ''),
                     'mob_no': customer_data.get('mob_no', ''),
                     'registration_no': customer_data.get('registration_no',''),
                     'pet_shop_name': customer_data.get('pet_shop_name', ''),
                     'email': customer_data.get('email', ''),
                     'education': customer_data.get('education', ''),
                     'status': customer_data.get('status', ''),
                     'type': customer_data.get('type', ''),
                     'addressl1': customer_data.get('addressl1', ''),
                     'addressl2': customer_data.get('addressl2', ''),
                     'Pin_code': customer_data.get('Pin_code', ''),
                     'State': customer_data.get('State', ''),
                     'geo_tag': customer_data.get('geo_tag', ''),
                     'District': customer_data.get('District', ''),
                     'taluka': customer_data.get('Taluka', ''),
                     'gst_no': customer_data.get('gst_no', ''),
                     'drug_licence_no': customer_data.get('drug_licence_no', ''),
                     'from_date': customer_data.get('from_date', ''),
                     'to_date': customer_data.get('to_date', ''),
                }
        elif cust_role_id in ['9']:
                meta_data = {
                     'cust_role': cust_role_id,
                     'cust_name': customer_data.get('cust_name', ''),
                     'email': customer_data.get('email', ''),
                     'mob_no': customer_data.get('mob_no', ''),
                     'addressl1': customer_data.get('addressl1', ''),
                     'addressl2': customer_data.get('addressl2', ''),
                     'Pin_code': customer_data.get('Pin_code', ''),
                     'State': customer_data.get('State', ''),
                     'geo_tag': customer_data.get('geo_tag', ''),
                     'District': customer_data.get('District', ''),
                     'taluka': customer_data.get('Taluka', ''),
                     'gst_no': customer_data.get('gst_no', ''),
                     'pan_card': customer_data.get('pan_card', ''),
                     'aadhar_card': customer_data.get('aadhar_card', ''),
                     'bank_name': customer_data.get('bank_name', ''),
                     'bank_ac_no': customer_data.get('bank_ac_no', ''),
                     'bank_ifsc': customer_data.get('bank_ifsc', ''),
                     'bank_address': customer_data.get('bank_address', ''),
                }
    
        for key, value in meta_data.items():
            CustomerMeta.objects.create(
                customer_id=customer.customer_id,
                customer_meta_key=key,
                customer_meta_value=value
            )

    def save_vetzone_meta(self, vetzone, customer_data):
        if not vetzone:
            return
        vetzone_meta_data = {
             
                'cust_name': customer_data.get('cust_name', ''),
                'mob_no': customer_data.get('mob_no', ''),
                'email': customer_data.get('email', ''),
                'addressl1': customer_data.get('addressl1', ''),
                'addressl2': customer_data.get('addressl2', ''),
                'State': customer_data.get('State', ''),
                'District': customer_data.get('District', ''),
                'Pin_code': customer_data.get('Pin_code', ''),
                'vetzone_type': customer_data.get('vetzone_type', ''),
                'total_number_MCC': customer_data.get('total_number_MCC', ''),
                'geo_tag': customer_data.get('geo_tag', ''),
                'total_milk_collection':customer_data.get('total_milk_collection', ''),
                'taluka':customer_data.get('taluka', ''),
                'Village':customer_data.get('Village', ''),
                
            }

        for key, value in vetzone_meta_data.items():
            VetzoneMeta.objects.create(
                vetzone_id=vetzone.vetzone_id,
                vetzone_meta_key=key,
                vetzone_meta_value=value
            )
