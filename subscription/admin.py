from django.contrib import admin
from .models import MembershipPlanModel,MemberSubscriptionModel
# Register your models here.
admin.site.register(MembershipPlanModel)
admin.site.register(MemberSubscriptionModel)
