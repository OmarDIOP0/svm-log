from django.urls import path
from log_analyzer import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logs/', views.log_list, name='log_list'),
    path('upload/', views.upload_logs, name='upload_logs'),
]