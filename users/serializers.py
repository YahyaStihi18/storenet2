from rest_framework import serializers
from .models import Account

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','phone','username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id','phone', 'username', 'email', 'password','first_name','last_name','wilaya','city','address','store_coordinates','documents1','documents2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(validated_data['email'],validated_data['username'],validated_data['phone'],validated_data['password'])

        return user