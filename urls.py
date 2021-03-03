from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from vsm import views

router = routers.DefaultRouter()
router.register(r'instruction', views.InstructionViewSet)
router.register(r'faq', views.FaqViewSet)
router.register(r'profiles', views.VSMProfileViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'holdings', views.HoldingViewSet)
router.register(r'leaders', views.LeaderViewSet)
router.register(r'leaders-iitb', views.IITBLViewSet)
router.register(r'tokens', views.ACTViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('me/', views.current_user),
    path('my-holdings/', views.my_holdings),
    path('trans/', views.make_transaction),
]