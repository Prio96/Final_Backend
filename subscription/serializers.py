from rest_framework import serializers
from . import models
from member.models import MemberModel
class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MembershipPlanModel
        fields='__all__'
        
class MemberSubscriptionSerializer(serializers.ModelSerializer):
    member=serializers.SlugRelatedField(
        queryset=MemberModel.objects.all(),
        slug_field='user__username',
    )
    plan=serializers.SlugRelatedField(
        queryset=models.MembershipPlanModel.objects.all(),
        slug_field='name'
    )
    class Meta:
        model=models.MemberSubscriptionModel
        fields='__all__'