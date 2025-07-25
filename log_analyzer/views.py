from django.shortcuts import render
from .models import AuthLog
from django.shortcuts import redirect
import pandas as pd
from datetime import datetime

def dashboard(request):
    total_logs = AuthLog.objects.count()
    malicious_logs = AuthLog.objects.filter(is_malicious=True).count()
    recent_logs = AuthLog.objects.order_by('-timestamp')[:10]
    
    return render(request, 'log_analyzer/dashboard.html', {
        'total_logs': total_logs,
        'malicious_logs': malicious_logs,
        'recent_logs': recent_logs,
    })

def log_list(request):
    logs = AuthLog.objects.all().order_by('-timestamp')
    return render(request, 'log_analyzer/log_list.html', {'logs': logs})


def upload_logs(request):
    if request.method == 'POST' and request.FILES.get('log_file'):
        # Lecture du fichier CSV
        df = pd.read_csv(request.FILES['log_file'])
        
        # Transformation des données
        for _, row in df.iterrows():
            AuthLog.objects.create(
                timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
                category=row['category'],
                source_ip=row['source_ip'],
                username=row.get('username'),
                status=row['status'],
                message=row['message'],
                raw_log=row['raw_log'],
                is_malicious=False  # Vous ajouterez la prédiction ici
            )
        
        return redirect('dashboard')
    return render(request, 'log_analyzer/upload.html')