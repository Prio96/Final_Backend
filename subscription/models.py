from django.db import models
from datetime import timedelta,date
from member.models import MemberModel
# Create your models here.
# PLAN_CHOICES=[
#         ('Weekly', 'Weekly'),
#         ('Monthly', 'Monthly'),
#         ('Yearly', 'Yearly')
#     ]
class MembershipPlanModel(models.Model):
    name=models.CharField(max_length=50)
    # description=models.TextField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    # duration=models.CharField(max_length=10, choices=PLAN_CHOICES)

    def __str__(self):
        return self.name

class MemberSubscriptionModel(models.Model):
    member=models.OneToOneField(MemberModel,related_name='member_plan',on_delete=models.CASCADE)
    plan=models.ForeignKey(MembershipPlanModel,related_name='subscriptions',on_delete=models.CASCADE)
    start_date=models.DateField(auto_now_add=True)
    # end_date=models.DateField()
    
    # def save(self, *args, **kwargs):
    #     if self.plan.duration=='Weekly':
    #         self.end_date=self.start_date+timedelta(weeks=1)
    #     elif self.plan.duration=='Monthly':
    #         self.end_date=self.start_date+timedelta(days=30)
    #     elif self.plan.duration=='Yearly':
    #         self.end_date=self.start_date+timedelta(days=365)
    #     super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.member.user.first_name} {self.member.user.last_name}- {self.plan.name} - {self.start_date}"
    # def is_active(self):
    #     return self.start_date<=date.today()<=self.end_date
    
    

    