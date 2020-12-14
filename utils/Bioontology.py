from external import *
from ontologies.models import Ontology
import xml.etree.ElementTree as ET


new_person = Ontology(
    class_id="class",
    parent_id="parent",
    label='Britney',
    definition='test definition',
    synonymous=["dummy", 3, 4],
    is_a=[2, 3, 4],
    has_a=[2, 3, 4])

# new_person.save()


class Bioontology:

    def __init__(self, owl_file, rdf_file):
        self.owl_file = owl_file
        self.rdf_file = rdf_file
        tree = ET.parse(rdf_file)
        self.rdf = tree.getroot()

    def start_iteration(self):
        namespaces = {'owl': 'http://www.w3.org/2002/07/owl#',
                      'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
                      }  # add more as needed
        counter = 1
        # iterate all classes inside rdf file
        for item in self.rdf.findall('owl:Class', namespaces):
            counter = counter + 1
            print(counter)
            # print the tag and text
            print('Big tag: ', item.tag)
            print('Big text: ', item.text)
            print('Big about: ', item.get('about'))
            print('Big attrib: ', item.attrib, end="\n\n")
            print('|----> Class id: ', item.attrib, end="\n\n")

            values_view = item.attrib.values()
            value_iterator = iter(values_view)
            first_value = next(value_iterator)
            print ("First: ", first_value)


bio = Bioontology("./utils/COVID-merged.owl", "./utils/owlapi.xrdf")
print(bio.owl_file, bio.rdf_file)

bio.start_iteration()
