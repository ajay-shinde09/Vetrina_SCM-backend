from rest_framework import serializers
from app.models import Suppliers

class SupplierDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['supplier_id', 'sup_name']
