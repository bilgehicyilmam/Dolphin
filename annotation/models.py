from django.db import models
from django.utils import timezone

class Annotation(models.Model):
    id = models.BigAutoField(primary_key=True)
    target_source = models.TextField(null=True)
    target_type = models.TextField(null=True)
    target_value = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now, null=True)
    creator_type = models.TextField(null=True)
    creator_email = models.TextField(null=True)
    creator_name = models.TextField(null=True)

    def __str__(self):
        return self.target_value

# Create your models here.
