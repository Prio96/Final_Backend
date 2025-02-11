from rest_framework import serializers
from . import models

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SpecializationModel
        fields='__all__'

class InstructorSerializer(serializers.ModelSerializer):
    specialization=serializers.StringRelatedField(many=True)
    class Meta:
        