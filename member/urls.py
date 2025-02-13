from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router=DefaultRouter()

router.register('members',views.MemberViewset)

urlpatterns = [
    path('',include(router.urls))
]