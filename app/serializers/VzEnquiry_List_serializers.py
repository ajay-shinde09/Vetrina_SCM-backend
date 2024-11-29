from rest_framework import serializers
from app.models import Vetzone, VetzoneHqDiv, Headquarters, VetzoneMeta

class VetzoneEnquirySerializer(serializers.ModelSerializer):
    sr_no = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()

    class Meta:
        model = Vetzone
        fields = ['sr_no', 'owner_name', 'place', 'mobile_number', 'approval_status', 'actions']

    def get_sr_no(self, obj):
        queryset = self.get_queryset().order_by('vetzone_id')
        for index, instance in enumerate(queryset, start=1):
            if instance == obj:
                return index
        return None

    def get_actions(self, obj):
        return {
            "read": f"/app/vetzone-enquiry/{obj.vetzone_id}/",
        }

    def get_place(self, obj):
        try:
            # Find the related HQ division
            hq_divs = VetzoneHqDiv.objects.filter(vetzone_id=obj.vetzone_id)
            if hq_divs.exists():
                # Get the first related HQ division
                hq_div = hq_divs.first()
                # Find the related headquarters
                hq = Headquarters.objects.get(hq_id=hq_div.hq_id)
                return hq.hq_name
            return None
        except Headquarters.DoesNotExist:
            return None

    def get_queryset(self):
        return Vetzone.objects.filter(approval_status='N')
    
from rest_framework import serializers
from app.models import Vetzone, VetzoneHqDiv, Headquarters,VetzoneMeta

class VetzoneEnquiryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vetzone
        exclude = ['password', 'type', 'role', 'kyc_status', 'approval_status', 'is_registered', 'created_on', 'placeorder', 'establishment_status']

    def update(self, instance, validated_data):
        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance