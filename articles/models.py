from django.utils import timezone
from django.db import models


class article(models.Model):

    pubmed_id = models.CharField(max_length=500, null=True)
    id = models.IntegerField(default=150000, primary_key=True)
    title = models.TextField(null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    keywords = models.JSONField(default=list, null=True)
    journal = models.TextField(null=True)
    publication_date = models.DateTimeField(default=timezone.now, null=True)
    authors = models.JSONField(default=list, null=True)
    conclusions = models.TextField(null=True)
    results = models.TextField(null=True)
    copyrights = models.TextField(null=True)
    doi = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.title



