from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from .models import UserProfile

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        user_profile = UserProfile(user=request.user)
        print(request.user.last_login, type(request.user.last_login))
        if user_profile.logged_in == False:
            user_profile.logged_in = False
            user_profile.save()
            path = "setup/daily-commit/"
        
        return path