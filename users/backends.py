from .models import Account
from django.core.exceptions import ValidationError



class AccountAuthBackend(object):

    def authenticate(self, request, username=None, password=None):
        try:
            user = Account.objects.get(email=username)
            if user.check_password(password):
                return user
            else:
                return None
        except:pass
        try:
            user = Account.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except:pass
        try:
            user = Account.objects.get(phone=username)
            if user.check_password(password):
                return user
            else:
                return None
        except Account.DoesNotExist:
            raise ValidationError("Invalid credentials")

    def get_user(self, user_id):
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None

