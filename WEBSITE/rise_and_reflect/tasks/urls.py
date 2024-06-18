from . import views
from django.urls import path

urlpatterns = [
    path('edit_all_tasks/<str:routine_type>/', views.edit_all_tasks, name='edit_all_tasks'),
    path('create_routine/<str:routine_type>/', views.create_tasks, name='create_routine'),
    path('order_tasks/<str:routine_type>/', views.order_tasks, name='order_tasks'),
    path('sort/', views.sort, name='sort'),
]
