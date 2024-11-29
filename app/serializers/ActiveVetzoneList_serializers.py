# serializers.py
from rest_framework import serializers

class ActiveVetzoneListSerializer(serializers.Serializer):
    sr_no = serializers.IntegerField()
    name = serializers.CharField()
    v_type_name = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    created_on = serializers.DateTimeField()
    approval_status = serializers.CharField()
    action = serializers.SerializerMethodField()

    def get_action(self, obj):
          return f'/app/Active-vetzone-DetailView/{obj["vetzone_id"]}/'
