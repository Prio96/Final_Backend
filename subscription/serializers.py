from rest_framework import serializers
from . import models

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MembershipPlanModel
        fields='__all__'
        
class MemberSubscriptionSerializer(serializers.ModelSerializer):
    member=serializers.StringRelatedField(many=False)
    plan=serializers.StringRelatedField(many=False)
    class Meta:
        model=models.MemberSubscriptionModel
        fields='__all__'