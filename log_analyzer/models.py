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
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.source_ip}"