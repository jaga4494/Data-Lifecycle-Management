from django.db import models
import ast
from django.contrib.postgres.fields import ArrayField, JSONField
from datetime import datetime, timezone
from django.utils.timezone import now
# Create your models here.
class User(models.Model):
    email = models.TextField(primary_key=True)
    name = models.TextField()
    accesskey = models.TextField(null=True)
    secretkey = models.TextField(null=True)
    def __str__(self):
        return self.email

def cycle_default():
    return {
        'start_time': [],
        'end_time': [],
        'frequency': []
    }

class Bucket(models.Model):
    email = models.TextField()
    bucket = models.TextField()
    object = models.TextField()
    creation_date = models.DateTimeField(null=True, blank=True, default=None)
    last_modified = models.DateTimeField()
    last_accessed = models.DateTimeField()
    count = models.IntegerField(default=1)
    frequency = models.FloatField(default=0)
    cycle = JSONField(blank=True, default= cycle_default)

    class Meta:
        unique_together = (("bucket", "object"),)