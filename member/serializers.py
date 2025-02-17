from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from member.models import MemberModel,GENDER_CHOICES

class MemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    user=serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    
    class Meta:
        model=models.MemberModel
        fields='__all__'
        
class MemberRegistrationSerializer(serializers.ModelSerializer):
    # User model fields
    username=serializers.CharField()
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    
    # Member model fields
    image=serializers.ImageField()
    mobile_no=serializers.CharField()
    gender=serializers.ChoiceField(choices=GENDER_CHOICES)
    weight=serializers.FloatField()
    height=serializers.FloatField()
    
    class Meta:
        model = MemberModel
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'password', 'confirm_password', 'image', 
            'mobile_no', 'gender', 'weight', 'height'
        ]
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match.'})
        if User.objects.filter(email=data['email']).exists:
            raise serializers.ValidationError({'error': 'Email already exists'})
        return data
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        user = User(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            email=email
        )
        user.set_password(password)
        user.save()
        
        member = MemberModel.objects.create(user=user, **validated_data)
        
        return member

