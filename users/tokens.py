from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from .models import Account

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, Account, timestamp):
        return (
            six.text_type(Account.pk) + six.text_type(timestamp) +
            six.text_type(Account.email_confirmed)
        )
account_activation_token = TokenGenerator()