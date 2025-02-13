from rest_framework import viewsets
from . import models
from . import serializers
from staff.permissions import IsStaff,UpdateOwnDetails

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import status
class MembershipPlanViewset(viewsets.ModelViewSet):
    queryset=models.MembershipPlanModel.objects.all()
    serializer_class=serializers.MembershipPlanSerializer
    
    def get_permissions(self):
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
    
    # def update(self, request, *args, **kwargs):
    #     instance=self.get_object()
    #     if is_member(request.user):
    #         if instance.member.user!=request.user:
    #             return Response({"error":"You can only update your own subscription"},status=status.HTTP_403_FORBIDDEN)
    #     return super().update(request, *args, **kwargs)
    
    