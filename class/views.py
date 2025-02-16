from django.shortcuts import render,redirect
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from staff.permissions import IsStaff,UpdateOwnDetails,IsMember
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from subscription.models import MemberSubscriptionModel
from staff.models import is_member
class SpecializationViewset(viewsets.ModelViewSet):
    queryset=models.SpecializationModel.objects.all()
    serializer_class=serializers.SpecializationSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class InstructorViewset(viewsets.ModelViewSet):
    queryset=models.InstructorModel.objects.all()
    serializer_class=serializers.InstructorSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class FitnessClassTimeViewset(viewsets.ModelViewSet):
    queryset=models.FitnessClassTimeModel.objects.all()
    serializer_class=serializers.FitnessClassTimeSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class FitnessClassViewset(viewsets.ModelViewSet):
    queryset=models.FitnessClassModel.objects.all()
    serializer_class=serializers.FitnessClassSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class FitnessClassBookingViewset(viewsets.ModelViewSet):
    queryset=models.FitnessClassBookingModel.objects.all()
    serializer_class=serializers.FitnessClassBookingSerializer
    def get_permissions(self):
        if self.action in ['create','update','partial_update','list','retrieve']:
            self.permission_classes=[IsAuthenticated,UpdateOwnDetails|IsStaff]
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if is_member(user):
            # Members can only see their own bookings
            return models.FitnessClassBookingModel.objects.filter(member__user=user)
        # Staff can see all bookings
        return super().get_queryset()
    
class BookClassOnlineAPIView(APIView):
    #This view is only applicable for members. Staffs will have to use FitnessClassBookingViewset to book someone.
    permission_classes=[IsAuthenticated,IsMember]
    
    def post(self,request,*args,**kwargs):
        user=request.user
        if not is_member(user):
            return Response({"error": "Only members can book classes."}, status=status.HTTP_403_FORBIDDEN)
        
        # Create the booking
        serializer = serializers.FitnessClassBookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        