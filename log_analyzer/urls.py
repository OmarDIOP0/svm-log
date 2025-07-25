from django.urls import path
from . import views
from . import tests

# app_name = 'log_analyzer'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logs/', views.log_list, name='logs_list'),
    path('logs/<int:pk>/', views.log_detail, name='log_detail'),
    path('upload/', views.upload_logs, name='upload_logs'),
    path('analyze/', views.analyze_logs, name='analyze_logs'),
]