from django.shortcuts import render,redirect
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from staff.permissions import IsStaff,UpdateOwnDetails,IsMember
from rest_framework.permissions import IsAuthenticated
from subscription.models import MemberSubscriptionModel
from staff.models import is_member
class SpecializationViewset(viewsets.ModelViewSet):
    queryset=models.SpecializationModel.objects.all()
    serializer_class=serializers.SpecializationSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsMember|IsStaff]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class InstructorViewset(viewsets.ModelViewSet):
    queryset=models.InstructorModel.objects.all()
    serializer_class=serializers.InstructorSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsMember|IsStaff]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class FitnessClassTimeViewset(viewsets.ModelViewSet):
    queryset=models.FitnessClassTimeModel.objects.all()
    serializer_class=serializers.FitnessClassTimeSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsMember|IsStaff]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class FitnessClassViewset(viewsets.ModelViewSet):
    queryset=models.FitnessClassModel.objects.all()
    serializer_class=serializers.FitnessClassSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsMember|IsStaff]
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
            # Members can only see their own subscriptions
            return models.FitnessClassBookingModel.objects.filter(member__user=user)
        # Staff can see all subscriptions
        return super().get_queryset()
    # Create action has been set in a way that user will be able to book class only using their own credentials. 
    # Even if they try to book classes using someone else's credentials, that will be ignored and the wrong credential will be overwritten by the actual user's credentials. 
    # Also the staff will be able to book classes using anyone's name
    def perform_create(self, serializer):
        user = self.request.user
        if is_member(user):
            member_instance = models.MemberModel.objects.get(user=user)
            serializer.save(member=member_instance)
        else:
            serializer.save()
        