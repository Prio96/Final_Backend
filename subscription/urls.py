from rest_framework.routers import DefaultRouter
from django.urls import path,include
from . import views

router=DefaultRouter()

router.register('plans',views.MembershipPlanViewset)
router.register('availed_subscriptions',views.MemberSubscriptionViewset)

urlpatterns = [
    path('',include(router.urls)),
    path('subscribe/',views.MemberSubscriptionAPIView.as_view(),name='subscribe'),
    path('update-subscription/',views.MemberSubscriptionAPIView.as_view(),name='update-subscription'),
]