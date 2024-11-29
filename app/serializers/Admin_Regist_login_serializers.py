import re
from rest_framework import serializers
from django.utils import timezone  
from app.models import Admin, AdminHqDiv, AdminMeta
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import authenticate
###########################################################

from django.contrib.auth.hashers import check_password

class AdminRegistrationSerializer(serializers.Serializer):
    STATE_CHOICES = [('Andhra Pradesh', 'Andhra Pradesh'),('Arunachal Pradesh', 'Arunachal Pradesh'),('Assam', 'Assam'),('Bihar', 'Bihar'),('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),('Gujarat', 'Gujarat'),('Haryana', 'Haryana'),('Himachal Pradesh', 'Himachal Pradesh'),('Jharkhand', 'Jharkhand'),('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),('Madhya Pradesh', 'Madhya Pradesh'),('Maharashtra', 'Maharashtra'),('Manipur', 'Manipur'),('Meghalaya', 'Meghalaya'),('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),('Odisha', 'Odisha'),('Punjab', 'Punjab'),('Rajasthan', 'Rajasthan'),('Sikkim', 'Sikkim'),('Tamil Nadu', 'Tamil Nadu'),
    ('Telangana', 'Telangana'),('Tripura', 'Tripura'),('Uttar Pradesh', 'Uttar Pradesh'),('Uttarakhand', 'Uttarakhand'),('West Bengal', 'West Bengal'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),('Chandigarh', 'Chandigarh'),('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Delhi', 'Delhi'),('Jammu and Kashmir', 'Jammu and Kashmir'),('Ladakh', 'Ladakh'),('Lakshadweep', 'Lakshadweep'),('Puducherry', 'Puducherry'),]
    sub_division_CHOICES=[('VetBiz','VetBiz'),('TredBiz','TredBiz'),('Canine','Canine'),('Poultry','Poultry')]
    admin_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()
    address = serializers.CharField()
    taluka = serializers.CharField()
    district = serializers.CharField()
    state = serializers.ChoiceField(choices=STATE_CHOICES)
    pin_code = serializers.IntegerField()
    geo_location = serializers.CharField(required=False, allow_blank=True)
    line_manager = serializers.IntegerField() 
    permission_id = serializers.IntegerField()
    created_by = serializers.IntegerField()
    hq_id = serializers.IntegerField()
    div_id = serializers.IntegerField()
    sub_division = serializers.ChoiceField(choices=sub_division_CHOICES)
    emp_id = serializers.CharField()
    mob_number_company = serializers.CharField()
    mob_number_personal = serializers.CharField()
    vetzone = serializers.IntegerField()
    profile_pic = serializers.ImageField(required=False)

    # def validate_password(self, value):
    #     """Validate the password for complexity."""
    #     if len(value) < 8:
    #         raise serializers.ValidationError("Password must be at least 8 characters long.")
    #     if not re.search(r'[A-Z]', value):
    #         raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    #     if not re.search(r'[a-z]', value):
    #         raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    #     if not re.search(r'\d', value):
    #         raise serializers.ValidationError("Password must contain at least one digit.")
    #     if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
    #         raise serializers.ValidationError("Password must contain at least one special character.")
    #     return value

    def create(self, validated_data):

        # Hash the password before saving it
        # hashed_password = make_password(validated_data['password'])

        admin = Admin.objects.create(
            admin_email=validated_data['admin_email'],
            username=validated_data['username'],  
            password=validated_data['password'],  
            line_manager=validated_data['line_manager'],  # Ensure line_manager is provided
            status='1',  # Assuming '1' means active
            is_block=validated_data.get('is_block', 'N'),  # Assuming '0' means not blocked
            permission_id=validated_data['permission_id'], 
            created_by=validated_data['created_by'], 
            created_date=timezone.now()
        )

        admin_meta = AdminMeta.objects.create(
            admin_id=admin.pk, 
            address=validated_data['address'],
            taluka=validated_data['taluka'],
            district=validated_data['district'],
            state=validated_data['state'],
            pin_code=validated_data['pin_code'],
            geo_location=validated_data.get('geo_location', ''),
            vetzone = validated_data['vetzone'],
            emp_id = validated_data['emp_id'],
            mob_number_company = validated_data['mob_number_company'],
            mob_number_personal = validated_data['mob_number_personal']
        )

        adminhqdiv = AdminHqDiv.objects.create( 
             admin_id=admin.pk,
             hq_id=validated_data['hq_id'],
             div_id=validated_data['div_id'],
             sub_division=validated_data['sub_division'],
         )

        return admin,admin_meta,adminhqdiv

# from django.core.cache import cache
# from django.utils import timezone
# from rest_framework import serializers
# from app.models import Admin
# from django.contrib.auth.hashers import check_password

# class AdminLoginSerializer(serializers.Serializer):
#     admin_email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         admin_email = data.get('admin_email')
#         password = data.get('password')

#         try:
#             admin = Admin.objects.get(admin_email=admin_email)
#         except Admin.DoesNotExist:
#             raise serializers.ValidationError("Invalid email.")

#         # Define cache keys
#         lock_key = f"{admin_email}_lock"
#         attempts_key = f"{admin_email}_attempts"
#         lock_until_key = f"{admin_email}_lock_until"

#         # Check if the account is locked
#         is_locked = cache.get(lock_key, False)
#         lock_until = cache.get(lock_until_key)

#         if is_locked:
#             if timezone.now() < lock_until:
#                 raise serializers.ValidationError("Account is locked due to multiple failed login attempts. Please try again later.")
#             else:
#                 # Unlock the account after the lock period expires
#                 cache.delete(lock_key)
#                 cache.delete(attempts_key)
#                 cache.delete(lock_until_key)

#         # Validate password
#         if not check_password(password, admin.password):
#             # Increment failed attempts
#             failed_attempts = cache.get(attempts_key, 0) + 1
#             cache.set(attempts_key, failed_attempts, timeout=3600)  # Cache timeout for 1 hour

#             if failed_attempts >= 5:
#                 # Lock the account if 5 failed attempts
#                 lock_until = timezone.now() + timezone.timedelta(hours=1)
#                 cache.set(lock_key, True, timeout=3600)
#                 cache.set(lock_until_key, lock_until, timeout=3600)
#                 raise serializers.ValidationError("Too many failed attempts. Account locked for 1 hour.")
#             else:
#                 raise serializers.ValidationError("Invalid password.")
#         else:
#             # On successful login, reset attempts and unlock if necessary
#             cache.delete(lock_key)
#             cache.delete(attempts_key)
#             cache.delete(lock_until_key)

#         # Include the admin instance in validated data
#         data['admin'] = admin
#         return data
from rest_framework import serializers
from django.core.cache import cache

class adminLoginSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class userLoginSerializer(serializers.Serializer):
    admin_email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    