from django.shortcuts import render
from .models import AuthLog
from django.shortcuts import redirect

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
        # Ici vous ajouterez le code pour traiter le fichier
        return redirect('dashboard')
    return render(request, 'log_analyzer/upload.html')