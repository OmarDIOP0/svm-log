from django.db import models
from django.utils import timezone

class AuthLog(models.Model):
    CATEGORY_CHOICES = [
        ('authentication-failed', 'Authentication Failed'),
        ('authentication-success', 'Authentication Success'),
        ('connection-closed', 'Connection Closed'),
        # Ajoutez toutes les autres catégories du modèle
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    source_ip = models.GenericIPAddressField()
    username = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20)
    message = models.TextField()
    raw_log = models.TextField()
    is_malicious = models.BooleanField(default=False)
    prediction_confidence = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Auth Log'
        verbose_name_plural = 'Auth Logs'

    def __str__(self):
        return f"{self.timestamp} - {self.source_ip} - {self.category}"