from django.db import models



class article(models.Model):

    pubmed_id = models.CharField(max_length=1000, null=False, primary_key=True )
    title = models.TextField(null=True)
    abstract = models.TextField(null=True)
    keywords = models.JSONField(default=list, null=True)
    journal = models.TextField(null=True)
    publication_date = models.CharField(max_length=1000, null=True)
    authors = models.JSONField(default=list, null=True)
    conclusions = models.TextField(null=True)
    results = models.TextField(null=True)
    copyrights = models.TextField(null=True)
    doi = models.CharField(max_length=1000, null=True)



