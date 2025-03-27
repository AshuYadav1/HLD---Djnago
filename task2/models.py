
from django.db import models

class Agency(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, unique=True)
    last_used = models.DateTimeField(auto_now=True)  # Updates on save
    load_factor = models.FloatField(default=0.0)     # Tracks usage load

    class Meta:
        indexes = [
            models.Index(fields=['api_key', 'load_factor'])
        ]  # Optimize queries

    def __str__(self):
        return self.name