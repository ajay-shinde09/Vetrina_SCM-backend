from rest_framework import serializers

class VetzoneSerializer(serializers.Serializer):
    sr_no = serializers.SerializerMethodField()
    vetzone_id = serializers.IntegerField()
    name = serializers.CharField()
    v_type_name = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    created_on = serializers.DateTimeField()
    closed_on = serializers.DateTimeField()
    remark = serializers.CharField(allow_blank=True, allow_null=True)
    approval_status = serializers.CharField()
    action = serializers.SerializerMethodField()

    def get_sr_no(self, obj):
        return obj.get('srno', None)

    def get_action(self, obj):
        # URL for the view button can be dynamically constructed
        return f'/app/Closed-vetzone-DetailView/{obj["vetzone_id"]}/'
