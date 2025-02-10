from django.db import models
from member.models import MemberModel
# Create your models here.
class MembershipPlanModel(models.Model):
    PLAN_CHOICES=[
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly')
    ]
    name=models.CharField(max_length=50)
    description=models.TextField()
    price=models.DecimalField(max_digits=8, decimal_places=2)
    duration=models.CharField(max_length=10, choices=PLAN_CHOICES)

    def __str__(self):
        return self.name

class MemberSubscriptionModel(models.Model):
    member=models.ForeignKey(MemberModel, )