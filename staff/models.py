from django.db import models
from django.contrib.auth.models import User
from member.models import MemberModel
from cloudinary.models import CloudinaryField
# from django.contrib.auth import get_user_model
# Create your models here.

class StaffModel(models.Model):
    user=models.OneToOneField(User,related_name='staff',on_delete=models.CASCADE)
    image=CloudinaryField('image')
    mobile_no=models.CharField(max_length=12)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# user=get_user_model()
def is_staff(user):
    return hasattr(user,'staff')

def is_member(user):
    return hasattr(user,'member')




    