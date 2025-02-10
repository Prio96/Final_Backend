from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MemberModel(models.Model):
    user=models.OneToOneField(User,related_name="member",on_delete=models.CASCADE)
    image=models.ImageField(upload_to="member/images/")
    mobile_no=models.CharField(max_length=12)
    weight=models.FloatField(help_text="Weight in kilograms")
    height=models.FloatField(help_text="Height in centimeters")
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    

