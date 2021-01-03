from external import *
from articles.models import article
from ontologies.models import Ontology
from datetime import datetime
import re
import uuid
from db import Database



class Annotation:
    article_id = "0"
    site_name = 'https://www.covidsearch.com'
    slug = 'articles'
    abstract = ''
    ontologies =  []
    ontology = None


    def __init__(self):
        self.set_ontologies()
   
    def create_annotation(self, article_id, abstract, article):

        self.article_id = article_id
        self.abstract = abstract
        if article_id != 0 and (abstract != '' or abstract != '') and len(self.ontologies) > 0:
            self.start_iteration()
        else:
            raise Exception('article_id should be different than 0 and abstract should not be empty.')
        if len(abstract) > len(self.abstract):
            raise Exception("Annotated article's length must be equal or greater than abstract")
        else:
            # good place to save to the database
            Database.insert('articles', {'pubmed_id': self.article_id, 'abstract': self.abstract })
            # print("Database insert id and new abstract: ", self.article_id, self.abstract)

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
        print('Count elements: ', len(ontologies))
        print(self.article_id, '\n')
        # start for loop for ontologies objects
        for ontology in ontologies:
            label = ontology.label
            
            abstract = self.abstract 
            found = abstract.find(label) # return an index number for label found
            if ( found != -1):
                self.ontology = ontology
                abstract = annotator.find_keyword(abstract, label)

    def find_keyword(self, text, label):
        """ annotate all occurences of a label """
        self.abstract = text

        i = 1
        while i == 1:
            x = re.search(rf"\b(?!>){label}\b(?!<)", self.abstract, re.IGNORECASE)
            if x:
                start = x.start()
                second_start = len(label) + start

                wrapper= self.create_wrapper(label)
                text = text[:start] + wrapper['wrapper'] + text[second_start:]

                self.abstract = text
                self.create_output(label, wrapper['idstamp'])
                # i = 0
            else:
                i = 0
        
         
    def find_abstracts(self, keyword):
        """  returns ids of abstracts found"""
        results = article.objects.filter(abstract__contains=keyword)
        print(len(search_result))
        print(search_result[0].abstract)
        abstract = search_result[0].abstract

    def create_stamp(self):
        # returns a time stamp with prefix

        prefix = 'covid19-'
        idstamp = prefix + str(uuid.uuid4())
        return idstamp

    def get_source(self):
        return '{}/{}/{}'.format(self.site_name, self.slug, self.article_id)

    def get_creator(self):
        return {'name': self.site_name}

    def get_created(self):
        now = datetime.now()
        now = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        return now

    def create_wrapper(self, keyword):
        """ returns a wrapper to replace"""
        # create timestamp
        idstamp = self.create_stamp()
        # returns a div element with idstamp and keyword
        wrapper = """<div id="{}">{}</div>""".format(idstamp, keyword)
        return {'wrapper': wrapper, 'idstamp' : idstamp}

    def save_annotation(self, abstract_id, ontology_id):
        head = self.create_head()
        target = self.create_target()
        body = self.create_body()
        output = self.create_output()
        save = self.save_annotation()
        pass
    
    def create_output(self, label, idstamp):
        annotation = dict()

        header = self.create_annotation_header(idstamp)
        annotation.update(header)
        
        target = self.create_annotation_target(idstamp)
        annotation.update(target)
        # if self.ontologies.label:
        body = self.create_annotation_body(label)
        annotation.update(body)

        footer = self.create_annotation_footer()
        annotation.update(footer)

        print(annotation)

        Database.insert('annotations', annotation)

        return annotation
    
    def create_output_alt(self, label, idstamp):
        # print(self.abstract_id)
        # print(self.abstract)
        has_body = True
        if has_body:
            return {
                    "@context": "http://www.w3.org/ns/anno.jsonld",
                    "id": idstamp,
                    "type": "Annotation",
                    "motivation": "describing",
                    "target": {
                        "source": self.get_source(),
                        "selector": {
                            "type": "CssSelector",
                            "value": "div#" + idstamp
                        }
                    },
                    "body": {
                        "type": "TextualBody",
                        "value": label,
                        "format": "text/plain",
                        "language": "en"
                    },
                    'created': self.get_created(),
                    'creator':  self.get_creator() 
                }
            
        else:
           return {
                    "@context": "http://www.w3.org/ns/anno.jsonld",
                    "id": idstamp,
                    "type": "Annotation",
                    "motivation": "describing",

                    'target': {
                        'source': self.get_source(),
                        'selector': {
                            'type': "CssSelector",
                            'value': "div#" + idstamp
                        }
                    },
                    'created': self.get_created(),
                    'creator':  self.get_creator() 
                }
       
    def create_annotation_header(self, idstamp):
            return {
                "@context": "http://www.w3.org/ns/anno.jsonld",
                "id": idstamp,
                "type": "Annotation",
                "motivation": "describing",
            }
    
    def create_annotation_target(self, idstamp):
            return {
                "target": {
                        "source": self.get_source(),
                        "selector": {
                            "type": "CssSelector",
                            "value": "div#" + idstamp
                        }
                    }
            }
            pass
    
    def create_annotation_body(self, label):
            body = []

            rdfs_label = {'label': label }
            body.append(rdfs_label)

            class_id = {'rdfs:Class': self.ontology.class_id }
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
    
annotator = Annotator()

""" Example #" : Creating annotaion with sample data """

abstract_id = "10203040"
sample = """Endemic is an  solution. novel coronavirus is an endemdic. global issue and having a negative
impact on the economy of the whole world. Like other countries, it also effected the economy and people of Pakistan. According to thn publicly reported
data, the first case of novel corona virus in Pakistan was reported on 27th
February 2020. The aim of the present study is to describe the mathematical
model and dynamics of COVID-19 in Pakistan. To investigate the spread of coronavirus in Pakistan, we develop the SEIR time fractional model with newly,
developed fractional operator of Atangana-Baleanu. We present briefly the analysis of the given model and discuss its applications using world health organization (WHO) reported data for Pakistan. We consider endemic the available infection cases from 19th March 2020, till 31st March 2020 and accordingly, various parameters are fitted or estimated. It is worth noting that we have calculated the basic reproduction number [Formula: see text] which shows that virus is spreading rapidly. Furthermore, stability analysis of the model at disease free equilibrium DFE andequilibriums EE is performed to observe the dynamics and transmission of the model. Finally, the AB fractional model is solved numerically. To show the effect of the various embedded parameters like fractional parameter [Formula: see text] on the model, various graphs are plotted. It is worth noting that the base of our investigation, we have predicted basic reproduction number the spread of disease for next 200 days a endemic.
"""

"""
print(annotator.create_annotation(abstract_id, sample))
"""

# print(annotator.abstract)

# annotator.find_keyword(sample, "endemic")

""" Example #2 """
all_articles = article.objects.all()[:100]
for article in all_articles:
    # print(article.abstract)
    if article.abstract != None:
        annotator.create_annotation(article.pubmed_id, article.abstract, article)
        # print(annotator.abstract)
        
# python ./utils/Annotator.py

""" Example 3 """
# my_object = annotator.find_keyword(sample, 'endemic')
# print(my_object)

""" Example 4 """
label = 'endemic'

# x = re.search(rf"\b(?!>){label}\b(?!<)", text, re.IGNORECASE)
# print(x)
# print(x.start())
# print(x.end())

# num_character = 20

# start1 = x.start() - num_character
# start2 = x.start()
# start1 = max(0, start1) # no negative

# end1 = x.end()
# end2 = x.end() + num_character

# prefix = text[start1:start2]
# suffix = text[end1:end2]

# print('prefix: ', prefix)

# print('exact: ', label)

# print('suffix: ', suffix)