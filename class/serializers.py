from rest_framework import serializers
from . import models

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SpecializationModel
        fields='__all__'

class InstructorSerializer(serializers.ModelSerializer):
    # specialization=serializers.StringRelatedField(many=True)
    class Meta:
        model=models.InstructorModel
        fields='__all__'
        
class FitnessClassTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.FitnessClassTimeModel
        fields='__all__'
    
class FitnessClassSerializer(serializers.ModelSerializer):
    # time=serializers.StringRelatedField(many=True)
    # instructor=serializers.StringRelatedField(many=False)
    # topic=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.FitnessClassModel
        fields='__all__'

class FitnessClassBookingSerializer(serializers.ModelSerializer):
    # class_session=serializers.StringRelatedField(many=False)
    # member=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.FitnessClassBookingModel
        fields='__all__'
        

        