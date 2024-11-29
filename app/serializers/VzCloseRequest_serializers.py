from rest_framework import serializers
from app.models import Vetzone

class VetzoneRemarkUpdateSerializer(serializers.ModelSerializer):

    vetzone_name = serializers.CharField()  # Accept the Vetzone name as input

    class Meta:
        model = Vetzone
        fields = ['vetzone_name', 'remark']

    def update(self, instance, validated_data):
        instance.remark = validated_data.get('remark', instance.remark)
        instance.save()
        return instance