from django.contrib import admin
from .models import FitnessClassBookingModel,FitnessClassModel,FitnessClassTimeModel,InstructorModel
# Register your models here.
admin.site.register(FitnessClassBookingModel)
admin.site.register(FitnessClassModel)
admin.site.register(FitnessClassTimeModel)
admin.site.register(InstructorModel)
