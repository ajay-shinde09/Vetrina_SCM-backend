# serializers.py
from rest_framework import serializers
from app.models import Customer

class CandFDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name']
