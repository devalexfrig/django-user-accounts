from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from account.conf import settings
from account.models import EmailAddress


class UsernameAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        try:
            user = User.objects.get(username__iexact=credentials["username"])
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(credentials["password"]):
                return user


class EmailAuthenticationBackend(ModelBackend):
    
    def authenticate(self, **credentials):
        try:
            email_address = EmailAddress.objects.get(email__iexact=credentials["username"], verified=True)
        except EmailAddress.DoesNotExist:
            return None
        else:
            user = email_address.user
            if user.check_password(credentials["password"]):
                return user
