from external import *
from articles.models import article
from ontologies.models import Ontology
from datetime import datetime
import re
import uuid
from db import Database


class Annotation:
    article_id = "0"
    site_name = 'http://localhost:3000'
    slug = 'article_detail'
    annotations_slug = 'http://localhost:4001/annotations'
    abstract = ''
    ontologies = []
    ontology = None
    last_id = 1

    # set ontologies for multiple uses
    def __init__(self):
        self.set_ontologies()

    # this starts a process of creating annotations for given article
    def create_annotation(self, article_id, abstract, article):
        """
        :param article_id:
        :param abstract: 
        :returns annotated abstract
        """
        self.article_id = article_id
        self.abstract = abstract
        if article_id != 0 and len(self.ontologies) > 0:
            self.start_iteration()
        else:
            raise Exception(
                'article_id should be different than 0 and abstract should not be empty.')
        if len(abstract) > len(self.abstract):
            raise Exception(
                "Annotated article's length must be equal or greater than abstract")
        else:
            return self.abstract

    # gets ontologies from the database and set as instance fields
    def set_ontologies(self):
        self.ontologies = self.get_ontologies()

    # gets all ontologies from the database
    def get_ontologies(self):
        """ returns all ontologies from the database """
        try:
            all_entries = Ontology.objects.all()
            return all_entries
        except:
            print('Database error!')

    # starts an iteration for each element of ontologies
    def start_iteration(self):
        # get ontologies from instance field
        ontologies = self.ontologies
        print('Ontologies count: ', len(ontologies))
        print(self.article_id, '\n')
        # start for loop for ontologies objects
        for ontology in ontologies:
            label = ontology.label
            abstract = self.abstract
            
            # return an index number for label found
            found = abstract.find(label)
            if (found != -1):
                self.ontology = ontology
                abstract = annotator.find_keyword(abstract, label)

    # annotate all occurences of a label
    def find_keyword(self, text, label):
        """
        :param text: annotate all occurences of a label 
        :param label:
        :returns 
        """
        self.abstract = text
        pattern = rf'\b(?!>){label}\b(?!<)'

        for match in re.finditer(pattern, text, re.IGNORECASE):
            # number of character to cut from left of the match
            num_character = 100

            # match start and end position
            s = match.start()
            e = match.end()

            # get left side of the match
            start1 = s - num_character
            start1 = max(0, start1)  # no negative
            start2 = s

            # get right side of the match
            end1 = e
            end2 = e + num_character

            # create prefix, exact, and suffix for annotation target
            prefix = text[start1:start2]
            suffix = text[end1:end2]

            self.create_output(label, prefix, suffix)

    # returns an id with site name
    def create_stamp(self):
        idstamp = self.last_id
        self.last_id += 1
        return '{}/{}'.format(self.annotations_slug, idstamp)

    # gets the source for the annotation
    def get_source(self):
        return '{}/{}/{}'.format(self.site_name, self.slug, self.article_id)

    # creates creator field for the JSON-LD
    def get_creator(self):
        return {
            "id": "https://github.com/HBilge/Dolphin/releases/tag/v0.1.0",
            "type": "Software",
            "name": "Dolphin 0.1",
            "homepage": "https://github.com/HBilge/Dolphin"
        }

    # created a time for the created field of the json
    def get_created(self):
        now = datetime.now()
        now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        return now

    # this creates a comple annotatio noutput
    def create_output(self, label, prefix, suffix):
        """
        :param label:
        :param prefix:
        :param suffix:
        """
        annotation = dict()
        idstamp = self.create_stamp()

        header = self.create_annotation_header(idstamp)
        annotation.update(header)

        target = self.create_annotation_target(label, prefix, suffix)
        annotation.update(target)
        # if self.ontologies.label:
        body = self.create_annotation_body(label)
        annotation.update(body)

        footer = self.create_annotation_footer()
        annotation.update(footer)

        # save annotatiın to the database
        Database.insert('annotations', annotation)

        return annotation

    # creates an annotation header
    def create_annotation_header(self, idstamp):
        """
        :param idstamp: an IRI 
        :returns an object including @context, id, type, motivation
        """
        return {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": idstamp,
            "type": "Annotation",
            "motivation": "describing",
        }

    # creates the annotation target
    def create_annotation_target(self, label, prefix, suffix):
        """
        :param label:
        :param prefix:
        :param suffix:
        :returns
        """
        return {
            "target": {
                "source": self.get_source(),
                "selector": {
                    "type": "TextQuoteSelector",
                    "exact": label,
                    "prefix": prefix,
                    "suffix": suffix
                }
            }
        }

    # creates the annotation body
    def create_annotation_body(self, label):
        """
        :param label:
        :returns annotation body
        """
        body = []

        rdfs_label = {'label': label}
        body.append(rdfs_label)

        class_id = {'rdfs:Class': self.ontology.class_id}
        body.append(class_id)

        if len(self.ontology.parent_id) > 0:
            parent = {'rdfs:subClassOf': self.ontology.parent_id}
            body.append(parent)

        if self.ontology.definition != None:
            parent = {'obo:IAO_0000115': self.ontology.definition}
            body.append(parent)

        return {
            "body": body
        }

    def create_annotation_footer(self):
        return {
            'created': self.get_created(),
            'creator':  self.get_creator()
        }


annotator = Annotation()


""" Example #1
print(annotator.create_annotation(abstract_id, sample))
"""

""" Example #2 """
all_articles = article.objects.all()[:90000]
for article in all_articles:
    # print(article.abstract)
    if article.abstract != None:
        annotator.create_annotation(
            article.pubmed_id, article.abstract, article)
        # print(annotator.abstract)
