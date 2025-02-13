from rest_framework import serializers
from . import models
from django.contrib.auth.models import User

class MemberSerializer(serializers.ModelSerializer):
    # user=serializers.StringRelatedField(many=False)
    
    class Meta:
        model=models.MemberModel
        fields='__all__'

