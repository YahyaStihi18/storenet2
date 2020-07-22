from . import views
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/',include('djoser.urls')),
    path('api/',include('djoser.urls.authtoken')),

    path('api/server/',views.server,name='server'),
    path('api/profile/',views.profile,name='profile'),
    
    path('home/',views.home, name='home'),
    path('register/', views.registration_view,name='register'),
    path('logout/', views.Logout_view,name='logout'),
    path('login/',views.login_view,name='login'),

]

