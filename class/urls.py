from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router=DefaultRouter()

router.register('classes',views.FitnessClassViewset)
router.register('specialization',views.SpecializationViewset)
router.register('available_time',views.FitnessClassTimeViewset)
router.register('instructors',views.InstructorViewset)
router.register('bookings',views.FitnessClassBookingViewset)
urlpatterns = [
    path('',include(router.urls))
]