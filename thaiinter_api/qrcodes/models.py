import uuid
from django.db import models
from django.conf import settings

class MetalSheetRoof(models.Model):
    roof_type = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    quantity = models.IntegerField()
    qr_code_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class RoofType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RoofColor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RoofSize(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name