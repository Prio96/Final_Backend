from rest_framework import viewsets,status
from . import models
from . import serializers
from .permissions import IsStaff,DenyAll
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from member.serializers import UserSerializer,User

class StaffViewset(viewsets.ModelViewSet):
    queryset=models.StaffModel.objects.all()
    serializer_class=serializers.StaffSerializer
    permission_classes=[IsAuthenticated,IsStaff]
    parser_classes = (MultiPartParser, FormParser)
#This viewset is only for viewing available users by staffs and superuser in the system. There are Memberviewset and Staffviewset for other functions.     
class UserViewset(viewsets.ModelViewSet):
    queryset=models.User.objects.all()
    serializer_class=UserSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsStaff]
        else:
            self.permission_classes=[DenyAll]
        return super().get_permissions()      
#In DRF, upon registration, a user is created. And the user can be assigned a role(Member or staff) by going to Memberviewset and Staffviewset respectively by any staff or superuser. The registration view (exclusively for member in frontend) has been created at member.views    
class UserRegistrationApiView(APIView):
    serializer_class=serializers.RegistrationSerializer
    
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Your account has been created successfully."}, status=status.HTTP_201_CREATED)
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
                return Response({'error':"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        request.auth.delete()
        logout(request)
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        
        
        