from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from member.models import MemberModel,GENDER_CHOICES

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "username", "first_name", "last_name", "email"]
        
class MemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    user=UserSerializer()
    
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
        
    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        password=self.validated_data['password']
        
        #Password and confirm_password matching has been shifted to frontend for avoiding lag of calling API
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        account=User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.save()
        
        MemberModel.objects.create(
            user=account,
            image=self.validated_data.get('image'),
            mobile_no=self.validated_data.get('mobile_no'),
            gender=self.validated_data.get('gender'),
            weight=self.validated_data.get('weight'),
            height=self.validated_data.get('height')    
        )
    

