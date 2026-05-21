from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('new/', views.skill_create, name='skill_create'),
    path('search/', views.skill_search, name='skill_search'),
    path('clusters/', views.clusters_view, name='clusters'),
]
