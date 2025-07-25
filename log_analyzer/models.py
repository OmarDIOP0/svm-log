from django.db import models
from django.utils import timezone
from . import tests

class AuthLog(models.Model):
    CATEGORY_CHOICES = [
        ('authentication-failed', 'Authentication Failed'),
        ('authentication-success', 'Authentication Success'),
        ('connection-closed', 'Connection Closed'),
        ('connection-failed', 'Connection Failed'),
        ('connection-opened', 'Connection Opened'),
        ('directory-changed', 'Directory Changed'),
        ('directory-created', 'Directory Created'),
        ('directory-deleted', 'Directory Deleted'),
        ('file-action-failure', 'File Action Failure'),
        ('file-deleted', 'File Deleted'),
        ('file-modification', 'File Modification'),
        ('file-read', 'File Read'),
        ('file-write', 'File Write'),
        ('hardware-monitoring', 'Hardware Monitoring'),
        ('http-request-failure', 'HTTP Request Failure'),
        ('http-request-success', 'HTTP Request Success'),
        ('ids-alert', 'IDS Alert'),
        ('network-filtered', 'Network Filtered'),
        ('network-traffic', 'Network Traffic'),
        ('process-ended', 'Process Ended'),
        ('process-error', 'Process Error'),
        ('process-info', 'Process Info'),
        ('process-shutdown', 'Process Shutdown'),
        ('process-started', 'Process Started'),
        ('system-configuration-changed', 'System Configuration Changed'),
        ('user-creation', 'User Creation'),
        ('user-deletion', 'User Deletion'),
        ('user-logout', 'User Logout'),
        ('user-session-open', 'User Session Open'),
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

