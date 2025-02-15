from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class MemberSerializer(serializers.ModelSerializer):
    user=serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    
    class Meta:
        model=models.MemberModel
        fields='__all__'

