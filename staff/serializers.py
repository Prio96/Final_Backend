from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class StaffSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    user=serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    
    class Meta:
        model=models.StaffModel
        fields='__all__'
    
    
        
class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','confirm_password']
    
    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        password=self.validated_data['password']
        password2=self.validated_data['confirm_password']
        
        if password!=password2:
            raise serializers.ValidationError({'error': 'Password does not match'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists"})
        
        account=User(username=username, email=email, first_name=first_name, last_name=last_name)
        account.set_password(password)
        account.save()
    
class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','password']