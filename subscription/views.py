from rest_framework import viewsets
from . import models
from . import serializers
from staff.permissions import IsStaff,UpdateOwnDetails
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import status
from member.models import MemberModel
from django.shortcuts import get_object_or_404
class MembershipPlanViewset(viewsets.ModelViewSet):
    queryset=models.MembershipPlanModel.objects.all()
    serializer_class=serializers.MembershipPlanSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
    
class MemberSubscriptionViewset(viewsets.ModelViewSet):
    queryset=models.MemberSubscriptionModel.objects.all()
    serializer_class=serializers.MemberSubscriptionSerializer
    
    def get_permissions(self):
        if self.action in ['list','retrieve','update','partial_update']:
            self.permission_classes=[IsAuthenticated,UpdateOwnDetails|IsStaff]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
    
   
    
    
    
