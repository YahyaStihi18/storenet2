from django.shortcuts import render,redirect,HttpResponse,reverse,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from users.forms import RegistrationForm,LoginForm
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from .serializers import ProfileSerializer,UserSerializer,AccountSerializer,AccountCreateSerializer
from .models import Account
from django.contrib import messages


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage,EmailMultiAlternatives,send_mail
from django.template.loader import get_template
from django.conf import settings





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
# Register API============================================
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            to_email = serializer.validated_data.get('email')
            user = request.user
            print(to_email)
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            }
            print('context done')

            with open( settings.BASE_DIR + "/users/templates/users/acc_active_email.txt" ) as f:
                text = f.read()
            message = EmailMultiAlternatives(subject=mail_subject,body=text,to=[to_email])
            html_template=get_template('users/acc_active_email.html').render(context)
            message.attach_alternative(html_template,"text/html")
            message.send()
            return HttpResponse("email sent")
        else:
            redirect('register')

#active view==========================================
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist ):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return HttpResponse('email confirmed')
    else:
        return HttpResponse('Activation link is expired or invalid!')



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

            
            


