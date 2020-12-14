from django.db import models

class Ontology(models.Model):
  id = models.BigAutoField(primary_key=True) #important
  label = models.CharField(max_length = 50, verbose_name = "Label")
  definition = models.CharField(max_length = 5000, verbose_name = "Definition")

  def __str__(self):
    return self.label
