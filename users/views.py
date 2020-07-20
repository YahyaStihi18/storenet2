from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, authenticate,logout
from users.forms import RegistrationForm,LoginForm

from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

def home(request):
    return HttpResponse("tihs is the home page")


#home api================================================
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

@api_view(['GET'])
def server(request):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = 'server is live,current time is'
    return Response(data=message+date, status=status.HTTP_200_OK)



# Register view============================================
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
           
            return redirect('home')
        else:
            context['Registration_form']= form
    else:
        form = RegistrationForm()
        context['Registration_form']= form
    return render(request,'users/register.html',context)


#login view===========================================
def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect("home")
    else:
        form = LoginForm()
    context['login_form'] = form
    return render(request,'users/login.html',context)

        


def Logout_view(request):
    logout(request)
    return redirect('home')

            
            


