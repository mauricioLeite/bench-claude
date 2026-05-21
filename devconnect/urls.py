from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('developers/', include('developers.urls')),
    path('skills/', include('skills.urls')),
    path('connections/', include('connections.urls')),
    path('dashboard/', include('dashboard.urls')),
]
