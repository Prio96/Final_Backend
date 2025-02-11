from rest_framework import serializers
from . import models

class MemberSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(many=False)
    
    class Meta:
        model=models.StaffModel
        fields='__all__'