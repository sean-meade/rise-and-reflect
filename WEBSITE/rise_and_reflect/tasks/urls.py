from . import views
from django.urls import path

urlpatterns = [
    path('create_routine/<str:routine_type>', views.create_routine, name='create_routine')
]
