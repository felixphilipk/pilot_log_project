from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.url),
    path('pilotlog/', include('pilotlog.urls')),
]
