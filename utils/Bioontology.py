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
        # add more as needed
        namespaces = {'owl': 'http://www.w3.org/2002/07/owl#',
                      'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
                      }
        counter = 1
        # iterate all classes inside rdf file
        for item in self.rdf.findall('owl:Class', namespaces):
            counter = counter + 1
            class_id = self.get_class_id(item)
            parent_id = self.get_parent_id(item)
            parents = self.get_parents(item)
            label = self.get_label(item)
            definition = self.get_definiton(item)
            synonymous = self.get_synonymous(item)
            print("\n")

            # prepare data
            new_ontology = Ontology(
                class_id = class_id,
                parent_id = parent_id,
                label = label,
                definition = definition,
                synonymous = synonymous,
                is_a = [2, 3, 4],
                has_a = [2, 3, 4]
            )

            # save database
            new_ontology.save()

    def get_class_id(self, item):
        # gets first value from a key/value pair of a list
        class_id = self.handle_first_value(item)
        print('class_id: ', class_id)
        return class_id

    def get_parent_id(self, item):
        parent_id = item.find(
            '{http://www.w3.org/2000/01/rdf-schema#}subClassOf')
        parent_id = self.handle_first_value(parent_id)
        print("parent_id: ", parent_id)
        return parent_id

    def get_parents(self, item):
        # prepare an empty array
        parents = []
        elements = item.findall(
            '{http://www.w3.org/2000/01/rdf-schema#}subClassOf')

        for el in elements:
            parent = el.attrib.values()
            parent = list(parent)
            print("parent", parent)
            if len(parent) >= 1:
                parent = parent[0]
                parents.append(parent)

        print(parents)
        return parent

    def get_label(self, item):
        label = item.find('{http://www.w3.org/2000/01/rdf-schema#}label').text
        print('label: ', label)
        return label

    def get_definiton(self, item):
        definiton = item.find('{http://purl.obolibrary.org/obo/}IAO_0000115')
        if definiton is not None:
            # prevents error
            definiton = definiton.text
            # utf8 check for printing to console
            print(definiton.encode('utf8'))
        return definiton

    def get_synonymous(self, item):
        # prepare an empty array
        syns = []
        syn = item.findall(
            '{http://www.geneontology.org/formats/oboInOwl#}hasExactSynonym')
        if syn is not None:
            for element in syn:
                # fill the array
                syns.append(element.text)
            print(syns)
        return syns

    def handle_first_value(self, item):
        return next(iter(item.attrib.values()))


bio = Bioontology("./utils/COVID-merged.owl", "./utils/owlapi.xrdf")

bio.start_iteration()
