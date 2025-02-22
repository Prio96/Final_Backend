from django.shortcuts import render,redirect
from rest_framework import viewsets,status
from . import models
from . import serializers
from .permissions import IsStaff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import request

class DebugTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        print("Authenticating with token")
        print("Authorization header (META):", request.META.get('HTTP_AUTHORIZATION'))
        print("Authorization header (request.headers):", request.headers.get('Authorization'))
        return super().authenticate(request)
class StaffViewset(viewsets.ModelViewSet):
    queryset=models.StaffModel.objects.all()
    serializer_class=serializers.StaffSerializer
    permission_classes=[IsAuthenticated,IsStaff]
    parser_classes = (MultiPartParser, FormParser)
    
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
                print("self.request.user:",self.request.user)
                print("self.request.user.auth_token:",self.request.user.auth_token)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':"Invalid Credentials"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    # def get(self,request):
    #     if request.user.is_authenticated:
    #         request.user.auth_token.delete()
    #         logout(request)
    #     return redirect("login")
    
    authentication_classes = [DebugTokenAuthentication]
    # permission_classes=[IsAuthenticated]  
    def get(self, request):
        print("Inside Logout")
        print("User:", request.user)
        print("Is Authenticated:", request.user.is_authenticated)
        print("Request Headers:", request.headers)  # Debugging
        
        if 'Authorization' not in request.headers:
            return Response({"error": "Authorization header is missing"}, status=400)
        if request.user.is_authenticated:
            request.auth.delete()
            logout(request)
            return Response({"message": "Successfully logged out"}, status=200)
        return Response({"error": "User is not authenticated"}, status=400)
       
        
        