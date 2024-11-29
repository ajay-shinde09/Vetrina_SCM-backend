# from rest_framework import serializers

# class EstablishmentPopupSerializer(serializers.Serializer):
#     vetzone_id = serializers.IntegerField()
#     vetzone_name = serializers.CharField()
#     sim_number = serializers.IntegerField(required=False, allow_null=True)
#     opening_goods = serializers.CharField(required=False, allow_null=True)
#     machine = serializers.CharField(required=False, allow_null=True)
#     machine_file = serializers.CharField(required=False, allow_null=True)
#     furniture = serializers.CharField(required=False, allow_null=True)
#     furniture_file = serializers.CharField(required=False, allow_null=True)

#     def to_representation(self, instance):
#         # Ensure only vetzone_id and vetzone_name are populated, other fields are set to null
#         data = super().to_representation(instance)
#         data['sim_number'] = None
#         data['opening_goods'] = None
#         data['machine'] = None
#         data['machine_file'] = None
#         data['furniture'] = None
#         data['furniture_file'] = None
#         return data
from rest_framework import serializers

class EstablishmentPopupSerializer(serializers.Serializer):
    vetzone_id = serializers.IntegerField()
    vetzone_name = serializers.CharField()
    sim_number = serializers.IntegerField(required=False, allow_null=True)
    opening_goods = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    machine = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    machine_file = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    furniture = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    furniture_file = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def to_representation(self, instance):
        # Ensure only vetzone_id and vetzone_name are populated, other fields are set to null
        data = super().to_representation(instance)
        data['sim_number'] = None
        data['opening_goods'] = None
        data['machine'] = None
        data['machine_file'] = None
        data['furniture'] = None
        data['furniture_file'] = None
        return data
