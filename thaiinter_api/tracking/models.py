from django.db import models
from django.conf import settings

class RoofTracking(models.Model):
    qr_code_id = models.UUIDField()
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    process_name = models.CharField(max_length=100)
    note = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

class ProcessName(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name