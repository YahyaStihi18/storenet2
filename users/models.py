from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, username, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
            password=password
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email",max_length=60, unique=True)
    username = models.CharField(max_length=60,unique=True)
    phone = models.CharField(max_length=60,unique=True)

    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone']
    

    objects = MyAccountManager()

    def __str__(self):
        return self.username
        
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(Account,on_delete=models.CASCADE,null=True, blank=True)
    first_name = models.CharField(max_length=60,blank=False)
    last_name = models.CharField(max_length=60,blank=False)
    wilaya = models.CharField(max_length=60,blank=False)
    city = models.CharField(max_length=60,blank=False)
    address = models.CharField(max_length=200,blank=False)
    store_coordinates = models.CharField(max_length=60,blank=False)
    documents1 = models.CharField(max_length=60,blank=False)
    documents2 = models.CharField(max_length=60,blank=False)

    def __str__(self):
        return self.first_name
        
    
    

