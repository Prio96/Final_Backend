from django.shortcuts import render,redirect
from rest_framework import viewsets
from . import models
from . import serializers
from staff.permissions import IsStaff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


class MemberViewset(viewsets.ModelViewSet):
    queryset=models.MemberModel.objects.all()
    serializer_class=serializers.MemberSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'destroy', 'update', 'partial_update']:
            self.permission_classes=[IsAuthenticated,IsStaff]
        else:
            self.permission_classes=[IsAuthenticated]
        return super().get_permissions()
