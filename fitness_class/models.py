from django.db import models
from member.models import MemberModel
from cloudinary.models import CloudinaryField

# Create your models here.

class SpecializationModel(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class InstructorModel(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    image=CloudinaryField('image')
    phone=models.CharField(max_length=12)
    specialization=models.ManyToManyField(SpecializationModel)#Assuming an instructor can have variety of specializations
    bio=models.TextField()
    
    def __str__(self):
        return self.name
        
class FitnessClassTimeModel(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class FitnessClassModel(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    time=models.ManyToManyField(FitnessClassTimeModel)
    instructor=models.ForeignKey(InstructorModel,on_delete=models.CASCADE)
    topic=models.ForeignKey(SpecializationModel,on_delete=models.CASCADE)# A class has to be only on one topic/specialization but one topic can have many class objects

    def __str__(self):
        return self.name
    
class FitnessClassBookingModel(models.Model):
    class_session=models.ForeignKey(FitnessClassModel,on_delete=models.CASCADE) # A class (object) can have multiple bookings (objects)
    member=models.ForeignKey(MemberModel,on_delete=models.CASCADE)
    booking_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.user.first_name} {self.member.user.last_name} - {self.class_session.name} - {self.booking_date}"