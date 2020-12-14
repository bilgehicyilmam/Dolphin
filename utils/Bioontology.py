from external import *
from ontologies.models import Ontology

new_person = Ontology(
  class_id="class",
  parent_id="parent",
  label = 'Britney',
  definition ='test definition',
  synonymous = ["dummy",3,4],
  is_a = [2,3,4],
  has_a = [2,3,4])

new_person.save()

class Bioontology
  pass
