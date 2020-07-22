from djoser.serializers import UserCreateSerializer,UserSerializer
from rest_framework import serializers
from .models import Account,Profile



class AccountCreateSerializer (UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Account
        fields = ('email','username','phone','password')

class ProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# User Serializer
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email','phone')

