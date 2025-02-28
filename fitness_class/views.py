from rest_framework import viewsets,status
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from staff.permissions import IsStaff,IsMember,is_member
from rest_framework.permissions import IsAuthenticated,AllowAny
from member.models import MemberModel
from rest_framework.parsers import MultiPartParser,FormParser
class SpecializationViewset(viewsets.ModelViewSet):
    queryset=models.SpecializationModel.objects.all().prefetch_related('fitnessclassmodel_set')
    serializer_class=serializers.SpecializationSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class InstructorViewset(viewsets.ModelViewSet):
    queryset=models.InstructorModel.objects.all().prefetch_related('specialization')
    serializer_class=serializers.InstructorSerializer
    parser_classes = (MultiPartParser, FormParser)
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
    queryset=models.FitnessClassModel.objects.all().select_related('instructor','topic')
    serializer_class=serializers.FitnessClassSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[AllowAny]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
class FitnessClassBookingViewset(viewsets.ModelViewSet):
    queryset=models.FitnessClassBookingModel.objects.all().order_by("-booking_date")
    serializer_class=serializers.FitnessClassBookingSerializer
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            self.permission_classes=[IsAuthenticated,IsMember|IsStaff]
        else:
            self.permission_classes=[IsAuthenticated,IsStaff]
        return super().get_permissions()
    
    def get_queryset(self):
        user = self.request.user
        if is_member(user):
            # Members can only view their own bookings.
            return models.FitnessClassBookingModel.objects.filter(member__user=user)
        # Staff can see all bookings and manage those
        return super().get_queryset()
    
class BookClassOnlineAPIView(APIView):
    #This view is only applicable for members in frontend. Staffs will have to use FitnessClassBookingViewset to manage bookings.
    permission_classes=[IsAuthenticated,IsMember]
    
    def post(self,request):
        user=request.user
        class_name=request.data.get('class_session')#From frontend
        class_session=models.FitnessClassModel.objects.get(name=class_name)
        member_instance=MemberModel.objects.get(user=user)
        if models.FitnessClassBookingModel.objects.filter(class_session=class_session, member=member_instance).exists():
            return Response({"error":"You have already booked this class."},status=status.HTTP_400_BAD_REQUEST)#Shown directly as an error message in frontend
        booking=models.FitnessClassBookingModel.objects.create(
            class_session=class_session, member=member_instance
        )
        return Response({"success":"Class booked successfully", "booking_id":booking.id},status=status.HTTP_201_CREATED)#Shown directly as a success message in frontend
        
        
        