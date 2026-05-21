from django.urls import path
from . import views

urlpatterns = [
    path('', views.connection_list, name='connection_list'),
    path('new/', views.connection_create, name='connection_create'),
    path('<int:pk>/status/', views.connection_status_update, name='connection_status_update'),
]
