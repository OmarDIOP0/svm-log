import django_tables2 as tables
from .models import AuthLog

class LogTable(tables.Table):
    class Meta:
        model = AuthLog
        template_name = "django_tables2/bootstrap4.html"
        fields = ("timestamp", "category", "source_ip", "username", "is_malicious")
        attrs = {"class": "table table-hover"}