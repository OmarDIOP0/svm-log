from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import AuthLog
from .utils import load_model, parse_log_file,preprocess_text
import pandas as pd
from datetime import datetime, timedelta
import re
from django.db import models
from django_tables2 import RequestConfig
from .tables import LogTable
from . import tests
import json
from django.http import HttpResponse
from django.urls import reverse


def dashboard(request):
    # Statistiques principales
    total_logs = AuthLog.objects.count()
    malicious_logs = AuthLog.objects.filter(is_malicious=True).count()
    auth_failures = AuthLog.objects.filter(category='authentication-failed').count()
    
    # Derniers logs
    recent_logs = AuthLog.objects.order_by('-timestamp')[:10]
    
    # Statistiques par catégorie
    categories = AuthLog.objects.values('category').annotate(count=models.Count('id')).order_by('-count')[:5]
    
    # Top IPs suspectes
    suspicious_ips = AuthLog.objects.filter(is_malicious=True)\
                          .values('source_ip')\
                          .annotate(count=models.Count('id'))\
                          .order_by('-count')[:5]
    
    context = {
        'total_logs': total_logs,
        'malicious_logs': malicious_logs,
        'auth_failures': auth_failures,
        'recent_logs': recent_logs,
        'categories': categories,
        'suspicious_ips': suspicious_ips,
    }
    
    return render(request, 'log_analyzer/dashboard.html', context)

# def log_list(request):
#     logs = AuthLog.objects.all().order_by('-timestamp')
    
#     # Filtrage
#     category_filter = request.GET.get('category')
#     if category_filter:
#         logs = logs.filter(category=category_filter)
    
#     ip_filter = request.GET.get('ip')
#     if ip_filter:
#         logs = logs.filter(source_ip=ip_filter)
    
#     malicious_filter = request.GET.get('malicious')
#     if malicious_filter == 'true':
#         logs = logs.filter(is_malicious=True)
#     elif malicious_filter == 'false':
#         logs = logs.filter(is_malicious=False)
    
#     # Pagination
#     paginator = Paginator(logs, 25)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         'page_obj': page_obj,
#         'category_choices': AuthLog.CATEGORY_CHOICES,
#     }
    
#     return render(request, 'log_analyzer/log_list.html', context)

def log_detail(request, pk):
    log = AuthLog.objects.get(pk=pk)
    return render(request, 'log_analyzer/log_detail.html', {'log': log})

def upload_logs(request):
    if request.method == 'POST' and request.FILES.get('log_file'):
        log_file = request.FILES['log_file']
        try:
            # Charger le modèle
            model = load_model()
            
            # Lire et parser le fichier
            logs = parse_log_file(log_file)
            
            # Prédictions
            predictions = model.predict(logs['clean_log'])
            
            # Sauvegarder en base
            saved_count = 0
            for idx, log in enumerate(logs.itertuples()):
                AuthLog.objects.create(
                    timestamp=datetime.now(),
                    category=predictions[idx],
                    source_ip=log.source_ip,
                    username=log.username,
                    status='Analyzed',
                    message=log.message,
                    raw_log=log.raw_log,
                    is_malicious=(predictions[idx] in ['authentication-failed', 'connection-failed']),
                )
                saved_count += 1
            
            messages.success(request, f'Successfully uploaded and analyzed {saved_count} log entries.')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Error processing file: {str(e)}')
    
    return render(request, 'log_analyzer/upload.html')

# Dans views.py
def log_list(request):
    table = LogTable(AuthLog.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'log_analyzer/log_list.html', {'table': table})

SUSPICIOUS_CATEGORIES = [
    'authentication-failed',
    'connection-failed',
    'file-action-failure',
    'file-modification',
    'http-request-failure',
    'ids-alert',
    'process-error',
    'directory-deleted',
    'file-deleted'
]

def analyze_logs(request):
    # Récupération des statistiques par catégorie
    categories = AuthLog.objects.values('category').annotate(count=models.Count('id'))
    category_labels = [cat['category'] for cat in categories]
    category_data = [cat['count'] for cat in categories]
    
    # Statistiques pour la timeline (7 derniers jours)
    timeline_labels = []
    timeline_data = []
    for i in range(7):
        date = datetime.now() - timedelta(days=6-i)
        date_str = date.strftime('%Y-%m-%d')
        count = AuthLog.objects.filter(
            timestamp__date=date.date(),
            is_malicious=True
        ).count()
        timeline_labels.append(date_str)
        timeline_data.append(count)
    
    # Top 5 des catégories suspectes
    suspicious_stats = (
        AuthLog.objects
        .filter(category__in=SUSPICIOUS_CATEGORIES)
        .values('category')
        .annotate(count=models.Count('id'))
        .order_by('-count')[:5]
    )
    
    context = {
        'total_logs': AuthLog.objects.count(),
        'malicious_logs': AuthLog.objects.filter(is_malicious=True).count(),
        'suspicious_logs': AuthLog.objects.filter(category__in=SUSPICIOUS_CATEGORIES).count(),
        'normal_logs': AuthLog.objects.filter(is_malicious=False).exclude(category__in=SUSPICIOUS_CATEGORIES).count(),
        'recent_threats': AuthLog.objects.filter(is_malicious=True).order_by('-timestamp')[:5],
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'timeline_labels': json.dumps(timeline_labels),
        'timeline_data': json.dumps(timeline_data),
        'suspicious_stats': suspicious_stats,
    }
    return render(request, 'log_analyzer/analyze.html', context)