from rest_framework import serializers

class StateSerializer(serializers.Serializer):
    state_id = serializers.IntegerField()
    state_name = serializers.CharField(max_length=255)
