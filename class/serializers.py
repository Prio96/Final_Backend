from rest_framework import serializers
from . import models
from member.models import MemberModel
from staff.models import is_member
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.SpecializationModel
        fields='__all__'

class InstructorSerializer(serializers.ModelSerializer):
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
        slug_field='name'
    )
    class Meta:
        model=models.FitnessClassModel
        fields='__all__'

class FitnessClassBookingSerializer(serializers.ModelSerializer):
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
        user=self.context['request'].user
        member=MemberModel.objects.get(user=user)
        if models.FitnessClassBookingModel.objects.filter(class_session=data['class_session'],member=member).exists():
            raise serializers.ValidationError("You have already booked this class.")
        return data
    # Create action has been set in a way that a member will be able to book class only using their own credentials. 
    # Even if they try to book classes using someone else's credentials, that will be ignored and the wrong credential will be overwritten by the actual user's credentials. 
    # Also the staff will be able to book classes using anyone's name
    def create(self, validated_data):
        user = self.context['request'].user
        if is_member(user):
            member_instance = MemberModel.objects.get(user=user)
            validated_data['member']=member_instance
        return super().create(validated_data)
            
        

        