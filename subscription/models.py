from django.db import models
from member.models import MemberModel

class MembershipPlanModel(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.name

class MemberSubscriptionModel(models.Model):
    member=models.OneToOneField(MemberModel,related_name='member_plan',on_delete=models.CASCADE)
    plan=models.ForeignKey(MembershipPlanModel,related_name='subscriptions',on_delete=models.CASCADE)
    start_date=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.user.first_name} {self.member.user.last_name}- {self.plan.name} - {self.start_date}"
   
    
    

    