from rest_framework import serializers
from . import models
from member.models import MemberModel

class SpecializationSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()
    class Meta:
        model=models.SpecializationModel
        fields='__all__'

class InstructorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    specialization=serializers.SlugRelatedField(
        queryset=models.SpecializationModel.objects.all(),
        many=True,
        slug_field='name'
    )
    class Meta:
        model=models.InstructorModel
        fields='__all__'
        
class FitnessClassTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.FitnessClassTimeModel
        fields='__all__'
    
class FitnessClassSerializer(serializers.ModelSerializer):
    time=serializers.SlugRelatedField(
        queryset=models.FitnessClassTimeModel.objects.all(),
        many=True,
        slug_field='name'
    )
    instructor=serializers.SlugRelatedField(
        queryset=models.InstructorModel.objects.all(),
        many=False,
        slug_field='name'
    )
    
    topic=serializers.SlugRelatedField(
        queryset=models.SpecializationModel.objects.all(),
        many=False,
        slug_field='name'#slug_field override done by to_representation function
    ) 
    class Meta:
        model=models.FitnessClassModel
        fields='__all__'
    def to_representation(self, instance):
        
        data=super().to_representation(instance)
        topic_instance=instance.topic
        
        data['topic']={
            "name":topic_instance.name,
            "image":topic_instance.image.url,
        }
        return data
    
class FitnessClassBookingSerializer(serializers.ModelSerializer): #Only applicable to DRF interface. Has no connection with frontend
    class_session=serializers.SlugRelatedField(
        queryset=models.FitnessClassModel.objects.all(),
        many=False,
        slug_field='name'
    )
    member=serializers.SlugRelatedField(
        queryset=MemberModel.objects.all(),
        slug_field='user__username',
    )
    class Meta:
        model=models.FitnessClassBookingModel
        fields='__all__'
    def validate(self, data):
        if models.FitnessClassBookingModel.objects.filter(class_session=data['class_session'],member=data['member']).exists():
            raise serializers.ValidationError("You have already booked this class.")
        return data
    
            
        

        