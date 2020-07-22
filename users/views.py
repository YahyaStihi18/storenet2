from django.shortcuts import render,redirect,HttpResponse,reverse,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from users.forms import RegistrationForm,LoginForm
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from .serializers import ProfileSerializer,UserSerializer,AccountSerializer
from .models import Account



def home(request):
    return HttpResponse("tihs is the home page")


#home api================================================

@api_view(['GET'])
def server(request):
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = 'server is live,current time is'
    return Response(data=message+date, status=status.HTTP_200_OK)

#profile api===============================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])

def profile(request):
    #current_user = request.user
    user = request.user 
    if request.method == 'GET':
        account = Account.objects.filter(username=user)
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

            
            


