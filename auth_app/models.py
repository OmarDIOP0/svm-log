# auth_app/models.py
from django.db import models

class AuthLog(models.Model):
    timestamp = models.DateTimeField()
    category = models.CharField(max_length=50)
    source_ip = models.GenericIPAddressField()
    username = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20)
    message = models.TextField()
    raw_log = models.TextField()
    is_malicious = models.BooleanField(default=False)
    confidence_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['source_ip']),
            models.Index(fields=['username']),
            models.Index(fields=['is_malicious']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.source_ip} - {self.status}"

class Alert(models.Model):
    log = models.ForeignKey(AuthLog, on_delete=models.CASCADE)
    severity = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alert {self.id} - {self.severity}"