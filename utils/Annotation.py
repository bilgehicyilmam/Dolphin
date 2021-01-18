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
    slug = 'articles'
    annotations_slug = 'http://localhost:4001/annotations'
    abstract = ''
    ontologies = []
    ontology = None
    last_id = 1

    def __init__(self):
        self.set_ontologies()

    def create_annotation(self, article_id, abstract, article):

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

    def set_ontologies(self):
        self.ontologies = self.get_ontologies()

    def get_ontologies(self):
        """ returns all ontologies from the database """
        try:
            all_entries = Ontology.objects.all()
            return all_entries
        except:
            print('Database error!')

    def start_iteration(self):
        """ start a loop for ontologies collection """
        # get ontologies from database
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

    def find_keyword(self, text, label):
        """ annotate all occurences of a label """
        self.abstract = text
        print(text)
        pattern = rf'\b(?!>){label}\b(?!<)'

        for match in re.finditer(pattern, text, re.IGNORECASE):
            # number of character to cut from left of the match
            num_character = 100

            # match start and end position
            s = match.start()
            e = match.end()
            print('String match "%s" at %d:%d' % (text[s:e], s, e))

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

            # debug
            print('prefix: ', prefix)
            print('exact: ', label)
            print('suffix: ', suffix)

            # call annoation save
            print(self.create_output(label, prefix, suffix))

    def create_stamp(self):
        # returns an id with prefix

        # prefix = 'covid19-'
        # idstamp = str(uuid.uuid4())
        idstamp = self.last_id
        self.last_id += 1
        return '{}/{}'.format(self.annotations_slug, idstamp)

    def get_source(self):
        return '{}/{}/{}'.format(self.site_name, self.slug, self.article_id)

    def get_creator(self):
        return {
            "id": "https://github.com/HBilge/Dolphin/releases/tag/v0.1.0",
            "type": "Software",
            "name": "Dolphin 0.1",
            "homepage": "https://github.com/HBilge/Dolphin"
        }

    def get_created(self):
        now = datetime.now()
        now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        return now

    def save_annotation(self, abstract_id, ontology_id):
        pass

    def create_output(self, label, prefix, suffix):
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

        print(annotation)

        Database.insert('annotations', annotation)

        return annotation

    def create_annotation_header(self, idstamp):
        return {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": idstamp,
            "type": "Annotation",
            "motivation": "describing",
        }

    def create_annotation_target(self, label, prefix, suffix):
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

    def create_annotation_body(self, label):
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
all_articles = article.objects.all()[:1000]
for article in all_articles:
    # print(article.abstract)
    if article.abstract != None:
        annotator.create_annotation(
            article.pubmed_id, article.abstract, article)
        # print(annotator.abstract)
