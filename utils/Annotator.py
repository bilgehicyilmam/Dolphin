from external import *
from articles.models import article
from ontologies.models import Ontology
from datetime import datetime
import re
import uuid

class Annotator:

    def __init__(self):
        pass

    def blank_function(self):
        pass

    def get_ontologies(self):
        # returns all ontologies from the database

        all_entries = Ontology.objects.all()
        return all_entries

    def abstract_miner(self, text):
        # starts a loop for ontologies collection

        # get ontologies from database
        ontologies = self.get_ontologies()
        print('Count elements: ', len(ontologies))

        # start for loop for ontologies objects
        for ontology in ontologies:
            label = ontology.label 
            found = text.find(label) # return an index number for label found
            if ( found != -1):
                text = annotator.update_abstract(text, label)
        return text


    def update_abstract(self, text, label):
        # annotate all occurences of a label

        i = 0
        while( i <= len(text)):
            print('start while')
            index = sample.find(label, i)
            if index != -1:
                wrapper = self.create_wrapper(label)
                i = i + index + len(wrapper)
                print('label: ', label, 'index', index, 'wrapper len: ', len(wrapper))
                text = text[:index] + wrapper + text[(len(label)+index):]
                print(text)
            else:
                break
        return text

    def add_wrapper(self, index, text, label, wrapper):
        pass


    def search_keyword(self, keywords):
        # blank

        # Article.objects.filter(label__text_search='Paul Lennon')
        #  Entry.objects.filter(body_text__search='cheese')
        pass

    def find_abstracts(self, keyword):
        # returns ids of abstracts found

        results = article.objects.filter(abstract__contains=keyword)
        print(len(search_result))
        print(search_result[0].abstract)
        abstract = search_result[0].abstract

    def update_abstract_1(self, text, keyword, wrapper):
        abstract = text.replace(keyword, wrapper)
        return abstract

    def create_stamp(self):
        # returns a time stamp with prefix

        # now = datetime.now() # 2020-12-28 10:31:41.593198
        # timestamp = datetime.timestamp(now) # 1609140701.593198
        # timestamp = str(timestamp)
        # timestamp = timestamp.replace('.', '') # 1609140701593198
        prefix = 'covid19-'
        # idstamp = prefix + timestamp # covid19_1609140701593198
        idstamp = prefix + str(uuid.uuid4())
        return idstamp
    
    def create_wrapper(self, keyword):
        # returns a wrapper to replace

        # create timestamp
        idstamp = self.create_stamp()
        # returns a div element with idstamp and keyword
        wrapper = """<div id="{}">{}</div>""".format(idstamp, keyword)
        return wrapper

    def create_annotation(self, abstract_id, ontology_id):
        head = self.create_head()
        target = self.create_target()
        body = self.create_body()
        output = self.create_output()
        save = self.save_annotation()
        pass

    def save_annotation():
        pass
        
        

sample = """Recently, endemic novel coronavirus is an endemic global issue and having a negative
impact on the economy of the whole world. Like other countries, it also effected the economy and people of Pakistan. According to the publicly reported
data, the first case of novel corona virus in Pakistan was reported on 27th
February 2020. The aim of the present study is to describe the mathematical
model and dynamics of COVID-19 in Pakistan. To investigate the spread of coronavirus in Pakistan, we develop the SEIR time fractional model with newly,
developed fractional operator of Atangana-Baleanu. We present briefly the analysis of the given model and discuss its applications using world health organization (WHO) reported data for Pakistan. We consider the available infection cases from 19th March 2020, till 31st March 2020 and accordingly, various parameters are fitted or estimated. It is worth noting that we have calculated the basic reproduction number [Formula: see text] which shows that virus is spreading rapidly. Furthermore, stability analysis of the model at disease free equilibrium DFE and endemic equilibriums EE is performed to observe the dynamics and transmission of the model. Finally, the AB fractional model is solved numerically. To show the effect of the various embedded parameters like fractional parameter [Formula: see text] on the model, various graphs are plotted. It is worth noting that the base of our investigation, we have predicted basic reproduction number the spread of disease for next 200 days endemic.
    """

annotator = Annotator()

# annotator.abstract_miner(sample)

annotator.update_abstract(sample, "endemic")

# i = len(sample)
# while( i <= len(sample)):
#     print('start while')
#     index = sample.find(word, -i)

#     if index != -1:
#         i = i - index -len(word)
#         print(index)
#     else:
#         print('not found')
#         break

# print(sample.find(word, -50))






# search_result = article.objects.filter(abstract__search='basic reproduction number')

"""
Geriden takip edersek önüne ne eklediğimizin önemi yok.
    Böyle değilniş, aynısının simetrisiymiş.
"""