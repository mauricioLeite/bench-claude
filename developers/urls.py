from django.urls import path
from . import views
from skills import views as skills_views

urlpatterns = [
    path('', views.developer_list, name='developer_list'),
    path('new/', views.developer_create, name='developer_create'),
    path('<int:pk>/', views.developer_detail, name='developer_detail'),
    path('<int:pk>/edit/', views.developer_edit, name='developer_edit'),
    path('<int:pk>/delete/', views.developer_delete, name='developer_delete'),
    path('<int:pk>/skills/add/', skills_views.developer_skill_add, name='developer_skill_add'),
    path('<int:dev_pk>/skills/<int:pk>/edit/', skills_views.developer_skill_edit, name='developer_skill_edit'),
    path('<int:dev_pk>/skills/<int:pk>/delete/', skills_views.developer_skill_delete, name='developer_skill_delete'),
]
