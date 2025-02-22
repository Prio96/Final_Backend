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
from fitness_class.models import FitnessClassBookingModel
from fitness_class.serializers import FitnessClassBookingSerializer
class MemberViewset(viewsets.ModelViewSet):
    queryset=models.MemberModel.objects.all()
    serializer_class=serializers.MemberSerializer
    # def get_permissions(self):
    #     if self.action in ['list','retrieve']:
    #         self.permission_classes=[IsAuthenticated,IsStaff]
    #     return super().get_permissions()
    
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
    
class MemberProfileAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        user=request.user
        
        try:
            member=models.MemberModel.objects.get(user=user)
        except models.MemberModel.DoesNotExist:
            return Response({"error":"Member profile not found"},status=404)
        
        member_data=serializers.MemberSerializer(member).data
        
        bookings=FitnessClassBookingModel.objects.filter(member=member)
        booking_data=FitnessClassBookingSerializer(bookings, many=True).data
        
        return Response({"member":member_data,"bookings":booking_data})

        
        