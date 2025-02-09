from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MemberModel(models.Model):
    user=models.OneToOneField(User,related_name="member",on_delete=models.CASCADE)
    

