from external import *
from ontologies.models import Ontology
import xml.etree.ElementTree as ET
import uuid


class Bioontology:

    def __init__(self, owl_file, rdf_file):
        self.owl_file = owl_file
        self.rdf_file = rdf_file
        tree = ET.parse(rdf_file)
        self.rdf = tree.getroot()

    # Loops through complete xml data
    def start_iteration(self):
        """
        :return: Returns null
        """
        # add more as needed
        namespaces = {'owl': 'http://www.w3.org/2002/07/owl#',
                      'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
                      }
        # iterate all classes inside rdf file
        for item in self.rdf.findall('owl:Class', namespaces):
            class_id = self.get_class_id(item)
            parent_ids = self.get_parent_ids(item)
            label = self.get_label(item)
            definition = self.get_definiton(item)
            synonymous = self.get_synonymous(item)
            # save database
            self.db_save(class_id, parent_ids, label, definition, synonymous)

    # Saves extracted ontology data to the database
    def db_save(self, class_id, parent_ids, label, definition, synonymous):
        """
        :param class_id: The class id of thr ontology class
        :param parent_ids: This is a list including subClassOf property of the ontology class
        :param label: rdfs:label property  the ontology class
        :param definition: IAO000115 property of the ontology class
        :param synonymous: hasExactSynonym property of the ontology class
        """
        # prepare data
        new_ontology = Ontology(
            class_id=class_id,
            parent_id=parent_ids,
            label=label,
            definition=definition,
            synonymous=synonymous
        )
        new_ontology.save()

    # Extracts first value from a key/value pair of a list
    def get_class_id(self, item):
        """
        :param item: An ontology class
        :return: Return class name of an ontology
        """
        class_id = self.handle_first_value(item)
        return class_id

    # This method is used inside the iteration. Example element:
    # <rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/GO_0019048"/>
    def get_parent_id(self, item):
        """
        :param item: An ontology item
        :return: Returns subClassOf property of a class
        """
        parent_id = item.find(
            '{http://www.w3.org/2000/01/rdf-schema#}subClassOf')
        parent_id = self.handle_first_value(parent_id)
        return parent_id

    # This method takes an xml element and extracts subClassOf area
    # of the class. The element from the xml file is like:
    # <rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/GO_0019048"/>
    def get_parent_ids(self, item):
        """
        :param item: An ontology item
        :return: Returns a single sum value of all precipitation.
        """
        # prepare an empty array
        parents = []

        elements = item.findall(
            '{http://www.w3.org/2000/01/rdf-schema#}subClassOf')
        if elements is not None:
            for el in elements:
                parent = el.attrib.values()
                parent = list(parent)
                if len(parent) >= 1:
                    parent = parent[0]
                    parents.append(parent)
        return parents

    # This label will ve saved to database as label. And
    # it will be used for creating annotations. Example element:
    # <rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">suppression by virus of host translation</rdfs:label>
    def get_label(self, item):
        """
        :param item: An ontology item
        :return: <rdfs:label> of the xml
        """
        label = item.find('{http://www.w3.org/2000/01/rdf-schema#}label').text
        return label

    # Extract definition (IAO_0000115)
    def get_definiton(self, item):
        """
        :param item: An ontology item
        :return: Encoded version of the definition
        """
        definiton = item.find('{http://purl.obolibrary.org/obo/}IAO_0000115')
        if definiton is not None:
            # prevents error
            definiton = definiton.text
        return definiton

    # Extracts synonymous of an ontology
    def get_synonymous(self, item):
        """
        :param item: An ontology item
        :return: All synonymous of the class
        """
        # prepare an empty array
        syns = []
        syn = item.findall(
            '{http://www.geneontology.org/formats/oboInOwl#}hasExactSynonym')
        if syn is not None:
            for element in syn:
                # fill the array
                syns.append(element.text)
        return syns

    # An helper method
    def handle_first_value(self, item):
        return next(iter(item.attrib.values()))


# Initialize an instance
bio = Bioontology("./utils/COVID-merged.owl", "./utils/owlapi.xrdf")

# Start iteration for ontlogies
bio.start_iteration()
