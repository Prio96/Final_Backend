from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
# Create your models here.

class StaffModel(models.Model):
    user=models.OneToOneField(User,related_name='staff',on_delete=models.CASCADE)
    image=CloudinaryField('image')
    mobile_no=models.CharField(max_length=12)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"






    