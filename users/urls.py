from . import views
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [

    path('api/register/', views.register, name='register'),
    path('api/login/', obtain_auth_token,name='login'),
    path('api/server/',views.server,name='server'),
    path('api/profile/',views.profile,name='profile'),
    path('api/confirmation/',views.confirmation_api,name='confirmation'),
    path('api/activate/<uidb64>/<token>/',views.activate_api,name='activate'),

    
    path('home/',views.home, name='home'),
    path('register/', views.registration_view,name='register'),
    path('logout/', views.Logout_view,name='logout'),
    path('login/',views.login_view,name='login'),

]

