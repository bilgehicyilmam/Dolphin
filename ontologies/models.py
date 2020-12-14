from django.db import models
from djongo import models

class Ontology(models.Model):
  id = models.BigAutoField(primary_key=True) #important
  class_id = models.CharField(max_length = 500, null=True, verbose_name = "Class")
  parent_id = models.CharField(max_length = 500, null=True, verbose_name = "Subclass of")
  label = models.CharField(max_length = 500, verbose_name = "Label")
  definition = models.CharField(max_length = 5000, null=True, verbose_name = "Definition")
  synonymous = models.JSONField(default=list, null=True)
  is_a = models.JSONField(default=list, null=True)
  has_a = models.JSONField(default=list, null=True)

  def __str__(self):
    return self.label
