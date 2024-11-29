from rest_framework import serializers
from app.models import Divisions  # Assuming you have a model named Divisions

class DivisionDropDownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisions
        fields = ['division_id', 'division_name']
