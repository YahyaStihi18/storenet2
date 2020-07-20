from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, authenticate,logout
from users.forms import RegistrationForm,LoginForm

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


def home(request):
    return HttpResponse("tihs is the home page")
    
# Register API============================================
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

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

#logn API ==========================================
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
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

            
            


