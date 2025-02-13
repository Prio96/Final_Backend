from django.shortcuts import render,redirect
from rest_framework import viewsets
from . import models
from . import serializers
from .permissions import IsStaff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token

class StaffViewset(viewsets.ModelViewSet):
    queryset=models.StaffModel.objects.all()
    serializer_class=serializers.StaffSerializer
    def get_permissions(self):
        self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
    
class UserRegistrationApiView(APIView):
    serializer_class=serializers.RegistrationSerializer
    
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response("Your account has been created successfully")
        return Response(serializer.errors)

class UserLoginApiView(APIView):
    serializer_class=serializers.UserLoginSerializer
    def post(self,request):
        serializer=serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data['username']
            password=serializer.validated_data['password']
            
            user=authenticate(username=username, password=password)
            
            if user:
                token,_=Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request,user)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':"Invalid Credentials"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login")