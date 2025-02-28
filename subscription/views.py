from rest_framework import viewsets
from . import models
from . import serializers
from staff.permissions import IsStaff,IsMember
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import status
from staff.permissions import is_member
class MembershipPlanViewset(viewsets.ModelViewSet):
    queryset=models.MembershipPlanModel.objects.all()
    serializer_class=serializers.MembershipPlanSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
    
class MemberSubscriptionViewset(viewsets.ModelViewSet): #Only for DRF interface. There are options for members here too with only view restrictions
    queryset=models.MemberSubscriptionModel.objects.all()
    serializer_class=serializers.MemberSubscriptionSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsMember|IsStaff]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if is_member(user):
            # Members can only see their own plans
            return models.MemberSubscriptionModel.objects.filter(member__user=user)
        # Staff can see all plans and manage those
        return super().get_queryset()

class MemberSubscriptionAPIView(APIView): #For subscribing in frontend
    permission_classes=[IsAuthenticated,IsMember]
    def get(self, request):
        user=request.user
        try:
            subscription=models.MemberSubscriptionModel.objects.get(member=user.member)
            serializer=serializers.MemberSubscriptionSerializer(subscription)
            return Response({"success":"Got user's current plan","data":serializer.data},status=status.HTTP_200_OK)#Shown only in console of frontend if success
        except models.MemberSubscriptionModel.DoesNotExist:
            return Response({"error":"No active subscription"},status=status.HTTP_404_NOT_FOUND)#Shown directly as an error message in frontend
        
    def post(self, request):
        user=request.user
        plan_id=request.data.get('plan')#From frontend
        plan=models.MembershipPlanModel.objects.get(id=plan_id)
        subscription,created=models.MemberSubscriptionModel.objects.get_or_create(member=user.member,defaults={"plan":plan})
        
        if not created:
            return Response({"error":"You already have a subscription"},status=status.HTTP_400_BAD_REQUEST)#Shown directly as an error message in frontend
        
        serializer=serializers.MemberSubscriptionSerializer(subscription)
        return Response({"success":"Subscription successful!","data":serializer.data},status=status.HTTP_201_CREATED)#Shown directly as a success message in frontend
    
    def put(self, request):
        user=request.user
        try:
            subscription=models.MemberSubscriptionModel.objects.get(member=user.member)
        except models.MemberSubscriptionModel.DoesNotExist:
            return Response({"error":"You don't have an active subscription."},status=status.HTTP_400_BAD_REQUEST)#Shown directly as an error message in frontend
        plan_id=request.data.get("plan")#From frontend
        new_plan=models.MembershipPlanModel.objects.get(id=plan_id)
        if subscription.plan==new_plan:
            return Response({"error":"Already subscribed to this plan."},status=status.HTTP_400_BAD_REQUEST)#Shown directly as an error message in frontend
        
        subscription.plan=new_plan
        subscription.save()
        serializer=serializers.MemberSubscriptionSerializer(subscription)
        return Response({"success":"Plan updated successfully!","data":serializer.data},status=status.HTTP_200_OK)#Shown directly as a success message in frontend
        
        
        
            

    
   
    
    
    
