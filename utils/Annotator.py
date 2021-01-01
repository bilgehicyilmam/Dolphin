from external import *
from articles.models import article
from ontologies.models import Ontology
from datetime import datetime
import re
import uuid

class Annotator:
    article_id = 0
    abstract = ''
    ontologies =  []

    def __init__(self):
        self.set_ontologies()
   
    def create_annotation(self, article_id, abstract):
        self.article_id = article_id
        self.abstract = abstract
        if article_id != 0 and (abstract != '' or abstract != '') and len(self.ontologies) > 0:
            self.start_iteration()
        else:
            raise Exception('article_id should be different than 0 and abstract should not be empty.')
        if len(abstract) > len(self.abstract):
            raise Exception("Annotated article's length must be equal or greater than abstract")
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
        print('Count elements: ', len(ontologies))
        print(self.article_id)
        print(self.abstract)
        # start for loop for ontologies objects
        for ontology in ontologies:
            label = ontology.label
            abstract = self.abstract 
            found = abstract.find(label) # return an index number for label found
            if ( found != -1):
                abstract = annotator.find_keyword(abstract, label)
    
    def find_keyword(self, text, label):
        """ annotate all occurences of a label """
        i = 0
        while( i <= len(text)):
            index = text.find(label, i)
            if index != -1:
                # create new wrapper
                wrapper= self.create_wrapper(label)
                i = i + index + len(wrapper)
                second_start = len(label) + index
                text = text[:index] + wrapper + text[second_start:]
            else:
                break
        self.abstract = text
        print("find_keyword executed")
        
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
    
    def create_wrapper(self, keyword):
        """ returns a wrapper to replace"""
        # create timestamp
        idstamp = self.create_stamp()
        # returns a div element with idstamp and keyword
        wrapper = """<div id="{}">{}</div>""".format(idstamp, keyword)
        return wrapper

    def save_annotation(self, abstract_id, ontology_id):
        head = self.create_head()
        target = self.create_target()
        body = self.create_body()
        output = self.create_output()
        save = self.save_annotation()
        pass
    
    def create_output(self, idstamp, value):
        
        if has_body:
            return {
                 {
                    "@context": "http://www.w3.org/ns/anno.jsonld",
                    "id": "covid19-3f0156a4-1e5f-4ea4-9585-60ff4f531fc1",
                    "type": "Annotation",
                    "motivation": "describing",

                    "target": {
                        "source": "http://example.org/Emblem004.html",
                        "selector": {
                            "type": "CssSelector",
                            "value": "div#covid19-3f0156a4-1e5f-4ea4-9585-60ff4f531fc1"
                        }
                    },

                    "body": {
                        "type": "TextualBody",
                        "value": "Amygdala is the integrative center for emotions, emotional behavior, and motivation. If the brain is turned upside down the end of the structure continuous with the hippocampus is called the uncus. If you peel away uncus you will expose the amygdala which abuts the anterior of the hippocampus.",
                        "format": "text/plain",
                        "language": "la"
                    },

                    "created": "2017-01-26T17:30:04.639Z",
                    "creator": {
                        "type": "Person",
                        "email": "mailto:mara@example.org",
                        "name": "Mara"
                    }
                }
            }
        else:
            {
                    "@context": "http://www.w3.org/ns/anno.jsonld",
                    "id": "anno-01",
                    "type": "Annotation",
                    "motivation": "describing",

                    "target": {
                        "source": "http://example.org/Emblem004.html",
                        "selector": {
                            "type": "CssSelector",
                            "value": "div#leftAmigdala"
                        }
                    },
                    "created": "2017-01-26T17:30:04.639Z",
                    "creator": {
                        "type": "Person",
                        "email": "mailto:mara@example.org",
                        "name": "Mara"
                    }
                }
            
        
        
annotator = Annotator()

abstract_id = "10203040"
sample = """
Recently, endemic novel coronavirus is an endemic global issue and having a negative
impact on the economy of the whole world. Like other countries, it also effected the economy and people of Pakistan. According to the publicly reported
data, the first case of novel corona virus in Pakistan was reported on 27th
February 2020. The aim of the present study is to describe the mathematical
model and dynamics of COVID-19 in Pakistan. To investigate the spread of coronavirus in Pakistan, we develop the SEIR time fractional model with newly,
developed fractional operator of Atangana-Baleanu. We present briefly the analysis of the given model and discuss its applications using world health organization (WHO) reported data for Pakistan. We consider the available infection cases from 19th March 2020, till 31st March 2020 and accordingly, various parameters are fitted or estimated. It is worth noting that we have calculated the basic reproduction number [Formula: see text] which shows that virus is spreading rapidly. Furthermore, stability analysis of the model at disease free equilibrium DFE and endemic equilibriums EE is performed to observe the dynamics and transmission of the model. Finally, the AB fractional model is solved numerically. To show the effect of the various embedded parameters like fractional parameter [Formula: see text] on the model, various graphs are plotted. It is worth noting that the base of our investigation, we have predicted basic reproduction number the spread of disease for next 200 days a endemic.
"""

print(annotator.create_annotation(abstract_id, sample))

# print(annotator.abstract)

# annotator.find_keyword(sample, "endemic")


all_articles = article.objects.all()[:10]

for article in all_articles:
    print(article.abstract)
    if article.abstract != None:
        print(annotator.create_annotation(abstract_id, article.abstract))