from rest_framework import viewsets,status
from . import models
from . import serializers
from staff.permissions import IsStaff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from fitness_class.models import FitnessClassBookingModel
from fitness_class.serializers import FitnessClassBookingSerializer


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
            return Response({"success": "Your member account has been created successfully."}, status=status.HTTP_201_CREATED) #Shown in frontend after registration
        
        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST) #Same email error, shown in frontend
    
class MemberProfileAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        user=request.user
        
        try:
            member=models.MemberModel.objects.get(user=user)
        except models.MemberModel.DoesNotExist:
            return Response({"error":"Member profile unavailable"},status=status.HTTP_404_NOT_FOUND)#Shown in frontend if a staff or non-member user logs in instead of a member
        
        member_data=serializers.MemberSerializer(member).data
        
        bookings=FitnessClassBookingModel.objects.filter(member=member)
        booking_data=FitnessClassBookingSerializer(bookings,many=True).data
        
        return Response({"member":member_data,"bookings":booking_data})#Shown in console

        
        