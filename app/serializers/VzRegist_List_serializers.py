from rest_framework import serializers
from app.models import Vetzone

class VetzoneListSerializer(serializers.ModelSerializer):
    sr_no = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    class Meta:
        model = Vetzone
        fields = ['sr_no', 'name', 'type', 'email', 'mobile_number', 'created_on', 'approval_status', 'actions']

    def get_sr_no(self, obj):
        # Calculate the Sr. No. based on the position of the object in the queryset
        #request = self.context.get('request')
        queryset = self.get_queryset().order_by('vetzone_id')
        for index, instance in enumerate(queryset, start=1):
            if instance == obj:
                return index
        return None

    def get_actions(self, obj):
        return {
            "read": f"/app/vetzone-RegistList-VetzoneDetails/{obj.vetzone_id}/"
        }

    def get_queryset(self):
        # Return the queryset used for Sr. No calculation
        return Vetzone.objects.filter(approval_status='F')