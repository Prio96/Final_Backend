from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GENDER_CHOICES=[
    ('Female','Female'),
    ('Male','Male')
]
class MemberModel(models.Model):
    user=models.OneToOneField(User,related_name="member",on_delete=models.CASCADE)
    image=models.ImageField(upload_to="member/images/")
    mobile_no=models.CharField(max_length=12)
    gender=models.CharField(max_length=8,choices=GENDER_CHOICES)
    weight=models.FloatField(help_text="Weight in kilograms")
    height=models.FloatField(help_text="Height in centimeters")
    date_joined=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    
    
    

