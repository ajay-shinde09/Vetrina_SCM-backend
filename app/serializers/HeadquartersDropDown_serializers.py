from rest_framework import serializers
from app.models import Headquarters

class HeadquartersDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Headquarters
        fields = ['hq_id', 'hq_name']
