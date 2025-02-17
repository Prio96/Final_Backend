from django.shortcuts import render,redirect
from rest_framework import viewsets
from . import models
from . import serializers
from staff.permissions import IsStaff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.parsers import MultiPartParser, FormParser

class MemberViewset(viewsets.ModelViewSet):
    queryset=models.MemberModel.objects.all()
    serializer_class=serializers.MemberSerializer
    permission_classes=[IsAuthenticated,IsStaff]
    parser_classes = (MultiPartParser, FormParser)
    

class MemberRegistrationApiView(APIView):
    serializer_class = serializers.MemberRegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Your account has been created successfully."}, status=201)
        
        return Response(serializer.errors, status=400)
