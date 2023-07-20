from . import views
from django.urls import path

urlpatterns = [
    path('daily-commit-submit/', views.submit_commitments, name='daily-commit-submit'),
    path('health-area/', views.health_areas, name='health-areas'),
    # TODO: Is it possible to shorten this url? Maybe in settings?
    path('accounts/login/setup/daily-commit/', views.submit_commitments, name='daily-commit')
]
