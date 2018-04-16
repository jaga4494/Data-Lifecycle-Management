from django.db import models

# Create your models here.
class User(models.Model):
    email = models.TextField(primary_key=True)
    name = models.TextField()
    accesskey = models.TextField(null=True)
    secretkey = models.TextField(null=True)
    def __str__(self):
        return self.email
