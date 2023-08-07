from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('custom_login.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('daily_commitments.urls')),
    path('tasks/', include('tasks.urls')),
    path('routine/', include('track_routine.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)