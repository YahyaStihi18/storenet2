from . import views
from django.urls import path,include

urlpatterns = [
    path('api/',include('djoser.urls')),
    path('api/',include('djoser.urls.authtoken')),

    path('api/server/',views.server,name='server'),
    
    #path('api/register/', RegisterAPI.as_view(), name='register'),
    #path('api/login2/', LoginAPI.as_view(), name='login'),
    #path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    #path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('home/',views.home, name='home'),
    path('register/', views.registration_view,name='register'),
    path('logout/', views.Logout_view,name='logout'),
    path('login/',views.login_view,name='login'),

]
