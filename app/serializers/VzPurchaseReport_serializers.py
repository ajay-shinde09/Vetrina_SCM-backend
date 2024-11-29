# delivery_challan_serializers.py

from rest_framework import serializers
from app.models import DeliveryChallan, Vetzone

class DeliveryChallanSerializer(serializers.ModelSerializer):
    sr_no = serializers.SerializerMethodField()
    vetzone_name = serializers.CharField(source='vetzone.name', read_only=True)  # Include Vetzone name

    class Meta:
        model = DeliveryChallan
        fields = ['sr_no', 'created_date', 'invoice_no', 'invoice_amount', 'vetzone_name']  # Add vetzone_name
    
    def get_sr_no(self, obj):
        # This will give a sequential number based on the queryset order
        return self.context['view'].get_srn_no()
