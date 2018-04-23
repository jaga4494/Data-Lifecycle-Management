from django.db import models
from django.utils.timezone import now
# Create your models here.
class User(models.Model):
    email = models.TextField(primary_key=True)
    name = models.TextField()
    accesskey = models.TextField(null=True)
    secretkey = models.TextField(null=True)
    def __str__(self):
        return self.email

class Bucket(models.Model):
    email = models.TextField()
    bucket = models.TextField()
    object = models.TextField()
    last_modified = models.DateTimeField()
    last_accessed = models.DateTimeField()
    count = models.IntegerField(default=1)

    class Meta:
        unique_together = (("bucket", "object"),)