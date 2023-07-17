from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from .models import UserProfile

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        user_profile = UserProfile(user=request.user)
        if user_profile.logged_in == False:
            # TODO: change to True when working properly with everything else
            user_profile.logged_in = False
            user_profile.save()
            path = "setup/daily-commit/"
        
        return path