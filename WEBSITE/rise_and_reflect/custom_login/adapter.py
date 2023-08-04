# from allauth.account.adapter import DefaultAccountAdapter
# from .models import UserProfile

# # Class to adapt the default function of allauth
# class MyAccountAdapter(DefaultAccountAdapter):

#     # Function to control where a user is sent when they login
#     def get_login_redirect_url(self, request):
#         # Grab the users Profile
#         user_profile = UserProfile(user=request.user)
#         # This checks if this is the first time the user logs in
#         if user_profile.logged_in == False:
#             # TODO: change to True when working properly so on second login user is sent somewhere else like profile page or routine page
#             user_profile.logged_in = False
#             user_profile.save()
#             path = "setup/daily-commit/"
        
#         return path