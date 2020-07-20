from .views import RegisterAPI
from . import views

from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),

    path('home/',views.home, name='home'),
    path('register/', views.registration_view,name='register'),
]
