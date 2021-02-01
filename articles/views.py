import itertools
import json

from bson import json_util
from django.shortcuts import render
from .models import *
from pymongo import MongoClient
import json
from django.shortcuts import render, redirect
from .models import article
from .forms import ArticleSearch
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pymongo import MongoClient
import re
from pprint import pprint
from django.shortcuts import get_object_or_404


cluster = MongoClient("mongodb+srv://dbuserdolphin:dbpassworddolphin@cluster0.h6bhx.mongodb.net/dolphin?retryWrites=true&w=majority")
db = cluster["dolphin"]
collection = db["articles_article"]
sys_collection = db["ontologies_ontology"]

cluster2 = MongoClient("mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net/<dbname>?retryWrites=true&w=majority")
db2 = cluster2["annotations"]
collection2 = db2["annotations"]

import datetime
import pycountry
from datetime import datetime

def all_articles(request):

    context = {}
    for i in range(50):
        context["articles_"+str(i)] = request.session.get("articles_"+str(i))



        dimensional_articles = context["articles_" + str(i)]
        paginated_articles = Paginator(dimensional_articles, 10)
        page_number = request.GET.get('page', None)
        article_page_ob = paginated_articles.get_page(page_number)

        for item in paginated_articles.object_list:
            authors = item['authors']
            keywords = item['keywords']
            b = json.loads(authors)
            c = json.loads(keywords)
            item['authors'] = b
            item['keywords'] = c

        context["article_page_ob_" + str(i)] = article_page_ob
        dimensional_articles.clear()

    return render(request, "all_articles.html", context)



def reqs(request):

    queries_0 = []
    queries_1 = []
    queries_2 = []
    queries_3 = []

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    country = request.GET.get('country')


    if 'q_0' in request.GET:
        query = request.GET["q_0"]
        queriess = [word.strip() for word in query.split(',')]
        queries_0 = queries_0 + queriess

    if 'q_1' in request.GET:
        query = request.GET["q_1"]
        queriess = [word.strip() for word in query.split(',')]
        queries_1 = queries_1 + queriess

    if 'q_2' in request.GET:
        query = request.GET["q_2"]
        queriess = [word.strip() for word in query.split(',')]
        queries_2 = queries_2 + queriess

    if 'q_3' in request.GET:
        query = request.GET["q_3"]
        queriess = [word.strip() for word in query.split(',')]
        queries_3 = queries_3 + queriess

    return queries_0, queries_1, queries_2, queries_3, start_date, end_date, country

def regex(query):

    last_query = []
    new_query=[]
    stopwords = ['and', 'or', 'but']
    for q in query:
        q = ' '.join(filter(lambda x: x not in stopwords,  q.split()))
        q = q.split(" ")
        new_query.append(q)
    for i in new_query:
        s = ""
        for j in i:
            if j == 'AND' or j == 'OR' or j == 'BUT':
                j = r'\b' + j + r'\b\W+(?:\w+\W+){0,4}?'
            else:
                j = r'(?i)\b' + j + r'\b\W+(?:\w+\W+){0,4}?'
            s = s + j
        last_query.append(s)

    return last_query


def synonymous(query):


    synonymouss = {}
    for index,q in enumerate(query):
        synonymous_words = []
        synonymous = sys_collection.find({"label": {"$regex": r'\b' + q + r'\b', "$options": 'i'}})
        for s in synonymous:
            for i in s["synonymous"]:
                synonymous_words.append(i)
        synonymouss["sys_" + str(index)] = synonymous_words

    return synonymouss

def query_process(query):

    new_query = []
    stopwords = ['and', 'or', 'but', 'And', 'But', 'Or']
    for q in query:
        q = ' '.join(filter(lambda x: x not in stopwords, q.split()))
        q = q.strip()
        new_query.append(q)
    return new_query

def parent_child(query):

    children = {}
    for index,q in enumerate(query):
        child_list = []
        a = collection2.find_one({"target.selector.exact": {"$regex": r'\b' + q + r'\b', "$options": 'i'}})
        if a is not None:
            c = a["body"][1]["rdfs:Class"]
            x = collection2.find({"body.rdfs:subClassOf": c })
            for i in x:
                child_list.append(i["target"]["selector"]["exact"])
            child_list = list(set(child_list))
            children["child_" + str(index)] = child_list

    return children

import string

def dimensional_search(request):

    global x
    context = {}
    index = 0
    sys_index = 0
    if request.GET:

        queries_0, queries_1, queries_2, queries_3, start_date, end_date, country = reqs(request)

        dt_start = start_date.replace("-", ", ")
        dt_start = dt_start.replace(" 0", " ")
        dt_end = end_date.replace("-", ", ")
        dt_end = dt_end.replace(" 0", " ")
        start_year, start_month, start_day = dt_start.split(", ", 2)
        end_year, end_month, end_day = dt_end.split(", ", 2)

        queries_0_processed = query_process(queries_0)
        queries_1_processed = query_process(queries_1)
        queries_2_processed = query_process(queries_2)
        queries_3_processed = query_process(queries_3)

        context["queries_0"] = queries_0
        context["queries_1"] = queries_1
        context["queries_2"] = queries_2
        context["queries_3"] = queries_3

        context["start_date"] = start_date
        context["end_date"] = end_date
        context["country"] = country

       # invalidcharacters = set(string.punctuation)

        counter = 0
        my_list = []

        invalidcharacters = {',', '\\', ']', "'", '=', '<', '+', '_', '`', ')', '@', '|', '/', '&', '#', '%', '}', '{', '-', '>', '*', ':', '?', '[', ';', '~', '!', '$', '.', '(', '^', '"'}

        for (a, i) in itertools.zip_longest(queries_0, queries_0_processed):

            articles = []
            context["q_" + str(index)] = [i]
            lists = []
            lists.append(a)
            lists = list(filter(None, lists))
            for que in lists:

                pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                quer2 = re.findall(pat, que)
                syn_reg = r'(?i)\b' + que + r'\b'
                syn_regex = re.compile(syn_reg)
                counter += 1
                que = re.findall(pat, que)
                pp = r''
                for qu in que:
                    if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                        po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                        tmp = pp + po
                        pp = tmp
                    else:
                        pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                        tmp = pp + pt
                        pp = tmp
                regex = re.compile(pp)
                articl = collection.find({"$and":
                                              [{"$or":
                                                    [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]},
                                               {"publication_date": {
                                                   "$gte": datetime(int(start_year), int(start_month), int(start_day),
                                                                    1, 30),
                                                   "$lte": datetime(int(end_year), int(end_month), int(end_day), 1,
                                                                    30)}},
                                               {"authors": {"$regex": country}}
                                               ]
                                          })

                sys_words = []
                synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                for s in synonymous:
                    for i in s["synonymous"]:
                        sys_words.append(i)
                my_list = my_list + sys_words

                context["syn_word_" + str(sys_index)] = i
                context["synonym_" + str(sys_index)] = sys_words

                tmp_syn = []
                for syn in sys_words:

                    if any(char in invalid_chars for char in syn):
                        continue
                    else:

                        syn = r'(?i)\b' + syn + r'\b'
                        syn = re.compile(syn)

                        articl2 = collection.find({"$and":
                                                       [{"$or": [{"abstract": {"$regex": syn}},
                                                                 {"title": {"$regex": syn}}]},
                                                        {"publication_date": {
                                                            "$gte": datetime(int(start_year), int(start_month),
                                                                             int(start_day), 1, 30),
                                                            "$lte": datetime(int(end_year), int(end_month), int(end_day), 1,
                                                                             30)}},
                                                        {"authors": {"$regex": country}}
                                                        ]
                                                   })
                        for i in articl2:
                            tmp_syn.append(i)

                child_words = []
                child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                if child is not None:
                    cl = child["body"][1]["rdfs:Class"]
                    sch = collection2.find({"body.rdfs:subClassOf": cl})
                    for i in sch:
                        child_words.append(i["target"]["selector"]["exact"])
                    child_words = list(set(child_words))

                context["child_word_" + str(sys_index)] = i
                context["children_" + str(sys_index)] = child_words

                tmp_child = []
                for chi in child_words:
                    if any(char in invalid_chars for char in chi):
                        continue
                    else:

                        chi = r'(?i)\b' + chi + r'\b'
                        chi = re.compile(chi)
                        articl3 = collection.find({"$and":
                                                       [{"$or": [{"abstract": {"$regex": chi}},
                                                                 {"title": {"$regex": chi}}]},
                                                        {"publication_date": {
                                                            "$gte": datetime(int(start_year), int(start_month),
                                                                             int(start_day), 1, 30),
                                                            "$lte": datetime(int(end_year), int(end_month),
                                                                             int(end_day), 1, 30)}},
                                                        {"authors": {"$regex": country}}
                                                        ]
                                                   })

                        for i in articl3:
                            tmp_child.append(i)

                if len(articles) == 0 and counter == 1:
                    for item in articl:
                        articles.append(item)
                    for it in tmp_syn:
                        if it in articles:
                            continue
                        else:
                            articles.append(it)
                    for chil in tmp_child:
                        if chil in articles:
                            continue
                        else:
                            articles.append(chil)
                else:
                    temp_arc = []
                    for a in articl:
                        if a in articles:
                            temp_arc.append(a)
                    for ite in tmp_syn:
                        if ite in articles and ite not in temp_arc:
                            temp_arc.append(ite)
                    for chill in tmp_child:
                        if chill in articles and chill not in temp_arc:
                            temp_arc.append(chill)
                    articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_1) >= 1:
            x = ""
            y = ""
            m = ""
            n = ""
            for (a, b, i, j) in itertools.zip_longest(queries_0, queries_1, queries_0_processed, queries_1_processed):


                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n

                if i is None:
                    context["q_" + str(index)] = [j]
                if j is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, j]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists = list(filter(None, lists))
                for que in lists:


                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp
                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day), 1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    context["syn_word_" + str(sys_index)] = j
                    context["synonym_" + str(sys_index)] = sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    context["child_word_" + str(sys_index)] = j
                    context["children_" + str(sys_index)] = child_words

                    tmp_child = []
                    for chi in child_words:

                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_2) >= 1:
            x = ""
            z = ""
            m = ""
            l = ""
            for (a, c, i, k) in itertools.zip_longest(queries_0, queries_2, queries_0_processed,
                                                      queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [k]
                if k is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp
                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    context["syn_word_" + str(sys_index)] = k
                    context["synonym_" + str(sys_index)] = sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    context["child_word_" + str(sys_index)] = k
                    context["children_" + str(sys_index)] = child_words

                    tmp_child = []
                    for chi in child_words:

                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_3) >= 1:
            x = ""
            p = ""
            m = ""
            q = ""
            for (a, d, i, w) in itertools.zip_longest(queries_0, queries_3, queries_0_processed,
                                                      queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if d is not None and w is not None:
                    p = d
                    q = w
                if d is None and w is None:
                    d = p
                    w = q

                if i is None:
                    context["q_" + str(index)] = [w]
                if w is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, w]

                articles = []
                lists = []
                lists.append(a)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    context["syn_word_" + str(sys_index)] = w
                    context["synonym_" + str(sys_index)] = sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    context["child_word_" + str(sys_index)] = w
                    context["children_" + str(sys_index)] = child_words

                    tmp_child = []
                    for chi in child_words:

                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_0) >= 1 and len(queries_1) >=1:
            queries_0 += [queries_0.pop(0)]
            queries_0_processed = query_process(queries_0)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, i, j) in itertools.zip_longest(queries_0, queries_1, queries_0_processed,
                                                      queries_1_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n

                if i is None:
                    context["q_" + str(index)] = [j]
                if j is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, j]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp
                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:
                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

            for (a, c, i, k) in itertools.zip_longest(queries_0, queries_2, queries_0_processed,
                                                      queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [k]
                if k is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:
                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0




        if len(queries_0) >= 2 and len(queries_1) >= 1:
            queries_0 += [queries_0.pop(0)]
            queries_0_processed = query_process(queries_0)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, i, j) in itertools.zip_longest(queries_0, queries_1, queries_0_processed,
                                                      queries_1_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n

                if i is None:
                    context["q_" + str(index)] = [j]
                if j is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, j]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

            for (a, c, i, k) in itertools.zip_longest(queries_0, queries_2, queries_0_processed,
                                                      queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [k]
                if k is None:
                    context["q_" + str(index)] = [i]
                else:
                    context["q_" + str(index)] = [i, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:

                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_1) >= 1:

            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                      queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp
                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:

                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_1) >= 1:
            queries_1 += [queries_1.pop(0)]
            queries_1_processed = query_process(queries_1)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp
                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_1) >= 2:
            queries_1 += [queries_1.pop(0)]
            queries_1_processed = query_process(queries_1)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)
                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_1) >= 3:
            queries_1 += [queries_1.pop(0)]
            queries_1_processed = query_process(queries_1)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_1) >= 4:
            queries_1 += [queries_1.pop(0)]
            queries_1_processed = query_process(queries_1)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)

                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_2) >= 1:
            queries_2 += [queries_2.pop(0)]
            queries_2_processed = query_process(queries_2)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_2) >= 2:
            queries_2 += [queries_2.pop(0)]
            queries_2_processed = query_process(queries_2)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_2) >= 3:
            queries_2 += [queries_2.pop(0)]
            queries_2_processed = query_process(queries_2)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_2) >= 4:
            queries_2 += [queries_2.pop(0)]
            queries_2_processed = query_process(queries_2)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_3) >= 1:

            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            for (a, b, d, i, j, g) in itertools.zip_longest(queries_0, queries_1, queries_3, queries_0_processed,
                                                            queries_1_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, g]
                if j is None:
                    context["q_" + str(index)] = [i, g]
                if g is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:

                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0
            z = ""
            l = ""

            for (a, c, d, i, j, k) in itertools.zip_longest(queries_0, queries_2, queries_3, queries_0_processed,
                                                            queries_2_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:
                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0



        if len(queries_3) >= 2:
            queries_3 += [queries_3.pop(0)]
            queries_3_processed = query_process(queries_3)
            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            for (a, b, d, i, j, g) in itertools.zip_longest(queries_0, queries_1, queries_3, queries_0_processed,
                                                            queries_1_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, g]
                if j is None:
                    context["q_" + str(index)] = [i, g]
                if g is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

            z = ""
            l = ""

            for (a, c, d, i, j, k) in itertools.zip_longest(queries_0, queries_2, queries_3, queries_0_processed,
                                                            queries_2_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:
                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_3) >= 3:
            queries_3 += [queries_3.pop(0)]
            queries_3_processed = query_process(queries_3)
            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            for (a, b, d, i, j, g) in itertools.zip_longest(queries_0, queries_1, queries_3, queries_0_processed,
                                                            queries_1_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, g]
                if j is None:
                    context["q_" + str(index)] = [i, g]
                if g is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

            z = ""
            l = ""

            for (a, c, d, i, j, k) in itertools.zip_longest(queries_0, queries_2, queries_3, queries_0_processed,
                                                            queries_2_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:
                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_3) >= 4:
            queries_3 += [queries_3.pop(0)]
            queries_3_processed = query_process(queries_3)
            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            for (a, b, d, i, j, g) in itertools.zip_longest(queries_0, queries_1, queries_3, queries_0_processed,
                                                            queries_1_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, g]
                if j is None:
                    context["q_" + str(index)] = [i, g]
                if g is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

            z = ""
            l = ""

            for (a, c, d, i, j, k) in itertools.zip_longest(queries_0, queries_2, queries_3, queries_0_processed,
                                                            queries_2_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:
                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_3) >= 1:

            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            z = ""
            l = ""

            for (a, b, c, d, i, j, k, g) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3, queries_0_processed,
                                                            queries_1_processed, queries_2_processed, queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k, g]
                if j is None:
                    context["q_" + str(index)] = [i, k, g]
                if g is None:
                    context["q_" + str(index)] = [i, j, k]
                else:
                    context["q_" + str(index)] = [i, j, k, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_3) >= 2:

            queries_3 += [queries_3.pop(0)]
            queries_3_processed = query_process(queries_3)

            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            z = ""
            l = ""

            for (a, b, c, d, i, j, k, g) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3,
                                                                  queries_0_processed,
                                                                  queries_1_processed, queries_2_processed,
                                                                  queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k, g]
                if j is None:
                    context["q_" + str(index)] = [i, k, g]
                if g is None:
                    context["q_" + str(index)] = [i, j, k]
                else:
                    context["q_" + str(index)] = [i, j, k, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1

                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_3) >= 3:

            queries_3 += [queries_3.pop(0)]
            queries_3_processed = query_process(queries_3)

            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            z = ""
            l = ""

            for (a, b, c, d, i, j, k, g) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3,
                                                                  queries_0_processed,
                                                                  queries_1_processed, queries_2_processed,
                                                                  queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k, g]
                if j is None:
                    context["q_" + str(index)] = [i, k, g]
                if g is None:
                    context["q_" + str(index)] = [i, j, k]
                else:
                    context["q_" + str(index)] = [i, j, k, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)
                    syn_reg = r'(?i)\b' + que + r'\b'
                    syn_regex = re.compile(syn_reg)
                    counter += 1
                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_3) >= 3:

            queries_3 += [queries_3.pop(0)]
            queries_3_processed = query_process(queries_3)

            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            z = ""
            l = ""

            for (a, b, c, d, i, j, k, g) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3,
                                                                  queries_0_processed,
                                                                  queries_1_processed, queries_2_processed,
                                                                  queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k, g]
                if j is None:
                    context["q_" + str(index)] = [i, k, g]
                if g is None:
                    context["q_" + str(index)] = [i, j, k]
                else:
                    context["q_" + str(index)] = [i, j, k, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


        if len(queries_0) >= 2:
            queries_0 += [queries_0.pop(0)]
            queries_0_processed = query_process(queries_0)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0


            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            z = ""
            l = ""

            for (a, b, c, d, i, j, k, g) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3,
                                                                  queries_0_processed,
                                                                  queries_1_processed, queries_2_processed,
                                                                  queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k, g]
                if j is None:
                    context["q_" + str(index)] = [i, k, g]
                if g is None:
                    context["q_" + str(index)] = [i, j, k]
                else:
                    context["q_" + str(index)] = [i, j, k, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        if len(queries_0) >= 3:
            queries_0 += [queries_0.pop(0)]
            queries_0_processed = query_process(queries_0)
            x = ""
            y = ""
            m = ""
            n = ""
            z = ""
            l = ""
            for (a, b, c, i, j, k) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_0_processed,
                                                            queries_1_processed, queries_2_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l

                if i is None:
                    context["q_" + str(index)] = [j, k]
                if j is None:
                    context["q_" + str(index)] = [i, k]
                if k is None:
                    context["q_" + str(index)] = [i, j]
                else:
                    context["q_" + str(index)] = [i, j, k]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)
                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

            x = ""
            y = ""
            m = ""
            n = ""
            u = ""
            t = ""
            z = ""
            l = ""

            for (a, b, c, d, i, j, k, g) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3,
                                                                  queries_0_processed,
                                                                  queries_1_processed, queries_2_processed,
                                                                  queries_3_processed):

                if a is not None and i is not None:
                    x = a
                    m = i
                if a is None and i is None:
                    a = x
                    i = m
                if b is not None and j is not None:
                    y = b
                    n = j
                if b is None and j is None:
                    b = y
                    j = n
                if c is not None and k is not None:
                    z = c
                    l = k
                if c is None and k is None:
                    c = z
                    k = l
                if d is not None and g is not None:
                    u = d
                    t = g
                if d is None and g is None:
                    d = u
                    g = t

                if i is None:
                    context["q_" + str(index)] = [j, k, g]
                if j is None:
                    context["q_" + str(index)] = [i, k, g]
                if g is None:
                    context["q_" + str(index)] = [i, j, k]
                else:
                    context["q_" + str(index)] = [i, j, k, g]

                articles = []
                lists = []
                lists.append(a)
                lists.append(b)
                lists.append(c)
                lists.append(d)
                lists = list(filter(None, lists))
                for que in lists:

                    pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                    quer2 = re.findall(pat, que)

                    syn_reg = r'(?i)\b' + que + r'\b'

                    syn_regex = re.compile(syn_reg)

                    counter += 1

                    que = re.findall(pat, que)

                    pp = r''
                    for qu in que:
                        if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                            po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + po
                            pp = tmp
                        else:
                            pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                            tmp = pp + pt
                            pp = tmp

                    regex = re.compile(pp)

                    articl = collection.find({"$and":
                                                  [{"$or":
                                                        [{"abstract": {"$regex": regex}},
                                                         {"title": {"$regex": regex}}]},
                                                   {"publication_date": {
                                                       "$gte": datetime(int(start_year), int(start_month),
                                                                        int(start_day),
                                                                        1, 30),
                                                       "$lte": datetime(int(end_year), int(end_month), int(end_day),
                                                                        1,
                                                                        30)}},
                                                   {"authors": {"$regex": country}}
                                                   ]
                                              })

                    sys_words = []
                    synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                    for s in synonymous:
                        for i in s["synonymous"]:
                            sys_words.append(i)
                    my_list = my_list + sys_words

                    tmp_syn = []
                    for syn in sys_words:

                        if any(char in invalid_chars for char in syn):
                            continue
                        else:

                            syn = r'(?i)\b' + syn + r'\b'
                            syn = re.compile(syn)

                            articl2 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": syn}},
                                                                     {"title": {"$regex": syn}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1,
                                                                                 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })
                            for i in articl2:
                                tmp_syn.append(i)

                    child_words = []
                    child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                    if child is not None:
                        cl = child["body"][1]["rdfs:Class"]
                        sch = collection2.find({"body.rdfs:subClassOf": cl})
                        for i in sch:
                            child_words.append(i["target"]["selector"]["exact"])
                        child_words = list(set(child_words))

                    tmp_child = []
                    for chi in child_words:
                        if any(char in invalid_chars for char in chi):
                            continue
                        else:

                            chi = r'(?i)\b' + chi + r'\b'
                            chi = re.compile(chi)
                            articl3 = collection.find({"$and":
                                                           [{"$or": [{"abstract": {"$regex": chi}},
                                                                     {"title": {"$regex": chi}}]},
                                                            {"publication_date": {
                                                                "$gte": datetime(int(start_year), int(start_month),
                                                                                 int(start_day), 1, 30),
                                                                "$lte": datetime(int(end_year), int(end_month),
                                                                                 int(end_day), 1, 30)}},
                                                            {"authors": {"$regex": country}}
                                                            ]
                                                       })

                            for i in articl3:
                                tmp_child.append(i)

                    if len(articles) == 0 and counter == 1:
                        for item in articl:
                            articles.append(item)
                        for it in tmp_syn:
                            if it in articles:
                                continue
                            else:
                                articles.append(it)
                        for chil in tmp_child:
                            if chil in articles:
                                continue
                            else:
                                articles.append(chil)
                    else:
                        temp_arc = []
                        for a in articl:
                            if a in articles:
                                temp_arc.append(a)
                        for ite in tmp_syn:
                            if ite in articles and ite not in temp_arc:
                                temp_arc.append(ite)
                        for chill in tmp_child:
                            if chill in articles and chill not in temp_arc:
                                temp_arc.append(chill)
                        articles = temp_arc

                searched_total_articles = len(articles)
                context["total_count_" + str(index)] = searched_total_articles

                index += 1
                sys_index += 1
                counter = 0

        for i in range(50):
            if "q_" + str(i) in context.keys():
                query_list = context["q_" + str(i)]
                t = "?abstract="
                for q in query_list:
                    term = q.split(" ")
                    for ter in term:
                        t = t + "+" + ter
                    t = t + "%2C"
                t = t[:-3]

                context["t_"+str(i)] = t



    return render(request, "dimension.html", {'context': context})




def parse_json(data):
    return json.loads(json_util.dumps(data))


def query_process(query):

    new_query = []
    stopwords = ['and', 'or', 'but', 'And', 'But', 'Or']
    for q in query:
        q = ' '.join(filter(lambda x: x not in stopwords, q.split()))
        new_query.append(q)
    return new_query

# Function for splitting query terms with commas

def split_line(query):
    result = [word.strip() for word in query.split(',')]
    return result

#Count function for dimensional search

def count(request):
        context = {}
        context["start_date"] = request.session.get("start_date")
        context["end_date"] = request.session.get("end_date")
        context["country"] = request.session.get("country")
        context["start_year"] = request.session.get("start_year")
        context["start_month"] = request.session.get("start_month")
        context["start_day"] = request.session.get("start_day")
        context["end_year"] = request.session.get("end_year")
        context["end_month"] = request.session.get("end_month")
        context["end_day"] = request.session.get("end_day")
        for i in range(50):
            context["q_" + str(i)] = request.session.get("q_" + str(i))
            lists = context["q_" + str(i)]
            start_date = context["start_date"]
            end_date = context["end_date"]
            country = context["country"]
            start_year = context["start_year"]
            start_month = context["start_month"]
            start_day = context["start_day"]
            end_year = context["end_year"]
            end_month = context["end_month"]
            end_day = context["end_day"]
            articles = []
            counter = 0
            my_list = []
            for que in lists:

                pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                quer2 = re.findall(pat, que)
                print(quer2)

                syn_reg = r'(?i)\b' + que + r'\b'
                print(syn_reg)


                syn_regex = re.compile(syn_reg)
                print(syn_regex)
                counter += 1
                print(counter)

                que = re.findall(pat, que)
                print(que)
                pp = r''
                for qu in que:
                    if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                        po = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                        tmp = pp + po
                        pp = tmp
                    else:
                        pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                        tmp = pp + pt
                        pp = tmp

                print(pp)
                regex = re.compile(pp)
                print(regex)

                print(start_year)

                articl = collection.find({"$and":
                                              [{"$or":
                                                    [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]},
                                               {"publication_date": {
                                                   "$gte": datetime(int(start_year), int(start_month), int(start_day),
                                                                    1, 30),
                                                   "$lte": datetime(int(end_year), int(end_month), int(end_day), 1,
                                                                    30)}},
                                               {"authors": {"$regex": country}}
                                               ]
                                          })

                sys_words = []
                synonymous = sys_collection.find({"label": {"$regex": syn_regex}})
                for s in synonymous:
                    for i in s["synonymous"]:
                        sys_words.append(i)
                my_list = my_list + sys_words

                tmp_syn = []
                for syn in sys_words:

                    syn = r'(?i)\b' + syn + r'\b'
                    syn = re.compile(syn)

                    print(syn)

                    articl2 = collection.find({"$and":
                                                   [{"$or": [{"abstract": {"$regex": syn}},
                                                             {"title": {"$regex": syn}}]},
                                                    {"publication_date": {
                                                        "$gte": datetime(int(start_year), int(start_month),
                                                                         int(start_day), 1, 30),
                                                        "$lte": datetime(int(end_year), int(end_month), int(end_day), 1,
                                                                         30)}},
                                                    {"authors": {"$regex": country}}
                                                    ]
                                               })
                    for i in articl2:
                        tmp_syn.append(i)

                child_words = []
                child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex}})
                # synonymous = collection2.find({"label": {"$regex": syn_regex}})
                if child is not None:
                    cl = child["body"][1]["rdfs:Class"]
                    sch = collection2.find({"body.rdfs:subClassOf": cl})
                    for i in sch:
                        child_words.append(i["target"]["selector"]["exact"])
                    child_words = list(set(child_words))
                tmp_child = []
                for chi in child_words:
                    print(chi)
                    chi = r'(?i)\b' + chi + r'\b'
                    chi = re.compile(chi)
                    articl3 = collection.find({"$and":
                                                   [{"$or": [{"abstract": {"$regex": chi}},
                                                             {"title": {"$regex": chi}}]},
                                                    {"publication_date": {
                                                        "$gte": datetime(int(start_year), int(start_month),
                                                                         int(start_day), 1, 30),
                                                        "$lte": datetime(int(end_year), int(end_month),
                                                                         int(end_day), 1, 30)}},
                                                    {"authors": {"$regex": country}}
                                                    ]
                                               })

                    for i in articl3:
                        tmp_child.append(i)

                    # for s in synonymous:
                    #    for i in s["synonymous"]:
                    #        sys_words.append(i)
                # articl = collection.find({"$and": [{"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]}, {"publication_date": {date}}]})
                if len(articles) == 0 and counter == 1:
                    # tmp_arc=[]
                    for item in articl:
                        articles.append(item)
                    for it in tmp_syn:
                        if it in articles:
                            continue
                        else:
                            articles.append(it)
                    for chil in tmp_child:
                        if chil in articles:
                            continue
                        else:
                            articles.append(chil)
                else:
                    temp_arc = []
                    for a in articl:
                        if a in articles:
                            temp_arc.append(a)
                    for ite in tmp_syn:
                        if ite in articles and ite not in temp_arc:
                            temp_arc.append(ite)
                    for chill in tmp_child:
                        if chill in articles and chill not in temp_arc:
                            temp_arc.append(chill)
                    articles = temp_arc

            searched_total_articles = len(articles)
            context["count_" + str(i)] = searched_total_articles

            request.session["count_" + str(i)] = context["count_" + str(i)]
        return render(request, {'context': context})

# Basic search function
def home(request):

#Transferred variables with request; query, start_date, end_date, country

    all_articles = article.objects.all()
    form = ArticleSearch()
    total_articles = all_articles.count()
    context = {
        "total_articles": total_articles,
        "form": form,
    }
    query = request.GET.get('abstract')
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')
    country = request.GET.get('country')
    global invalid_chars
    invalid_chars = {',', '\\', ']', "'", '=', '<', '+', '_', '`', ')', '@', '|', '/', '&', '#', '%', '}', '{', '-', '>', '*', ':', '?', '[', ';', '~', '!', '$', '.', '(', '^', '"'}


    if request.method == 'POST':

        pattern = r'(?i)\b' + query + r'\b'
        regex = re.compile(pattern)
        articles = []
        articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
        for item in articl:
            articles.append(item)

        searched_total_articles = articl.count()
        paginated_articles = Paginator(articles, 10)
        page_number = request.GET.get('page', None)
        article_page_ob = paginated_articles.get_page(page_number)
        context = {
            "total_articles": total_articles,
            "searched_articles": searched_total_articles,
            "articles": articles,
            "form": form,
            "article_page_ob": article_page_ob,
            "query": query
        }

# Recevived request method and processed thru from here

    elif request.method == 'GET':

# Query string is processed

        if query:
            queris = split_line(query)
            queris = list(filter(None, queris))
            dt_start = start_date.replace("-", ", ")
            dt_start= dt_start.replace(" 0", " ")
            dt_end = end_date.replace("-", ", ")
            dt_end = dt_end.replace(" 0", " ")
            start_year, start_month, start_day = dt_start.split(", ",2)
            end_year, end_month, end_day = dt_end.split(", ",2)
            articles = []
            counter = 0
            my_list=[]
            queris=query_process(queris)

# Regex is applied to process query term

            for que in queris:
                quer = ""
                pat = r'\b(?:(?!\band\b|\bor\b|\bbut\b|\bAnd\b|\bBut\b|\bOr\b)\w)+\b'
                quer2 = re.findall(pat, que)
                syn_reg= r'(?i)\b' + que + r'\b'

                syn_regex = re.compile(syn_reg)
                counter+= 1
                que = re.findall(pat, que)
                pp = r''
                for qu in que:
                    if qu == 'AND' or qu == 'OR' or qu == 'BUT':
                        po= r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                        tmp=  pp + po
                        pp=tmp
                    else:
                        pt = r'\b(?i:' + qu + r')(| |ing|ed|d)\b\W+(?:\w+\W+){0,4}?'
                        tmp= pp + pt
                        pp= tmp
                regex = re.compile(pp)

# Articles are collected based on the search term

                articl = collection.find({"$and":
                                              [{"$or":
                                                    [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]},
                                               {"publication_date": {"$gte": datetime(int(start_year), int(start_month), int(start_day), 1, 30), "$lte": datetime(int(end_year), int(end_month), int(end_day), 1, 30)}},
                                               {"authors": {"$regex": country}}
                                               ]
                                          })
                sys_words = []

# Synonmous words are found

                synonymous = sys_collection.find({"label": {"$regex": syn_regex }})
                for s in synonymous:
                    for i in s["synonymous"]:
                        sys_words.append(i)
                my_list = my_list+sys_words
                tmp_syn = []
                for syn in sys_words:
                    if any(char in invalid_chars for char in syn):
                        continue
                    else:
                        syn = r'(?i)\b' + syn + r'\b'
                        syn = re.compile(syn)

# Articles are collected based on the synonymous words

                        articl2 = collection.find({"$and":
                                                    [{"$or": [{"abstract": {"$regex": syn}}, {"title": {"$regex": syn}}]},
                                                        {"publication_date": {"$gte": datetime(int(start_year), int(start_month), int(start_day), 1, 30), "$lte": datetime(int(end_year), int(end_month), int(end_day), 1, 30)}},
                                                        {"authors": {"$regex": country}}
                                                        ]
                                                })
                        for i in articl2:
                            tmp_syn.append(i)

# Child classes of search terms are collected

                child_words = []
                child = collection2.find_one({"target.selector.exact": {"$regex": syn_regex }})
                if child is not None:
                    cl = child["body"][1]["rdfs:Class"]
                    sch = collection2.find({"body.rdfs:subClassOf": cl})
                    for i in sch:
                        child_words.append(i["target"]["selector"]["exact"])
                    child_words = list(set(child_words))
                tmp_child = []
                for chi in child_words:
                    print(chi)
                    if any(char in invalid_chars for char in chi):
                        continue
                    else:
                        chi = r'(?i)\b' + chi + r'\b'
                        chi = re.compile(chi)

# Articles are collected based on the child classes of the query term

                        articl3 = collection.find({"$and":
                                                        [{"$or": [{"abstract": {"$regex": chi}},
                                                                    {"title": {"$regex": chi}}]},
                                                        {"publication_date": {
                                                            "$gte": datetime(int(start_year), int(start_month),
                                                                                int(start_day), 1, 30),
                                                            "$lte": datetime(int(end_year), int(end_month),
                                                                                int(end_day), 1, 30)}},
                                                        {"authors": {"$regex": country}}
                                                        ]
                                                    })

                        for i in articl3:
                            tmp_child.append(i)

# Final collection of articles are formed here. Check is made to avoid duplicate articles for both query term
# and its synonyms and child classes.

                if len(articles) == 0 and counter == 1:
                    #tmp_arc=[]
                    for item in articl:
                        articles.append(item)
                    for it in tmp_syn:
                        if it in articles:
                            continue
                        else:
                            articles.append(it)
                    for chil in tmp_child:
                        if chil in articles:
                            continue
                        else:
                            articles.append(chil)
                else:
                    temp_arc=[]
                    for a in articl:
                        if a in articles:
                            temp_arc.append(a)
                    for ite in tmp_syn:
                        if ite in articles and ite not in temp_arc:
                            temp_arc.append(ite)
                    for chill in tmp_child:
                        if chill in articles and chill not in temp_arc:
                            temp_arc.append(chill)
                    articles = temp_arc

# Date info is collected for date graphical visualization

            dates=[]
            theCountries = []
            for art in articles:
                authors = art["authors"]
                for country in list(pycountry.countries):
                    if country.name in authors:
                        theCountries.append(country.name)

                date = art["publication_date"].strftime("%Y-%m-%d")

                dates.append(date)

# Country info is collected for graphical visualization based on affiliation country of the authors

            country_labels = {i: theCountries.count(i) for i in theCountries}

            sorted_countries = dict(sorted(country_labels.items(), key=lambda item: item[1]))


            date_labels = {i: dates.count(i) for i in dates}


            searched_total_articles = len(articles)

# Pagination of the pages are handled here.

            paginated_articles = Paginator(articles, 10)
            page_number = request.GET.get('page', None)
            country_new = request.GET.get('country', None)
            article_page_ob = paginated_articles.get_page(page_number)
            for item in paginated_articles.object_list:
                authors = item['authors']
                keywords = item['keywords']
                b = json.loads(authors)
                c = json.loads(keywords)
                item['authors'] = b
                item['keywords'] = c
            context = {
                "total_articles": total_articles,
                "searched_articles": searched_total_articles,
                "articles": articles,
                "form": form,
                "article_page_ob": article_page_ob,
                "query": query,
                "queris": queris,
                "my_list": my_list,
                "start_date": start_date,
                "end_date": end_date,
                "country": country_new,
                "country_labels": list(sorted_countries.keys()),
                "country_counts": list(sorted_countries.values()),
                "date_labels": list(date_labels.keys()),
                "date_counts": list(date_labels.values())
            }


    return render(request, "articles.html", context)

# Article detail page is defined here

def article_detail(request, pubmed_id):

# Required parameters are defined and assigned

    all_articles = article.objects.all()
    form = ArticleSearch(request.POST or None)
    total_articles = all_articles.count()
    detail_article = article.objects.get(pubmed_id = pubmed_id)
    idd = detail_article.id
    tit = detail_article.title
    abst = detail_article.abstract
    keyw = detail_article.keywords
    jour = detail_article.journal
    pub_date = detail_article.publication_date.date()
    auth = detail_article.authors
    conc= detail_article.conclusions
    res= detail_article.results
    copy = detail_article.copyrights
    dooi = detail_article.doi

    context = {
         "form": form,
         "idd" : idd,
         "tit" : tit,
         "abst" : abst,
         "keyw" : keyw,
         "jour" : jour,
         "pub_date" : pub_date,
         "auth" : auth,
         "conc" : conc,
         "res" : res,
         "copy" : copy,
         "dooi" : dooi,
         "pubmed_id" : pubmed_id
    }
    query = request.GET.get('abstract', '')
    if request.method == 'POST':

        pattern = r'(?i)\b' + query + r'\b'
        regex = re.compile(pattern)
        articles = []
        articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
        for item in articl:
            articles.append(item)

        searched_total_articles = articl.count()
        paginated_articles = Paginator(articles, 10)
        page_number = request.GET.get('page', None)
        article_page_ob = paginated_articles.get_page(page_number)
        context = {
            "total_articles": total_articles,
            "searched_articles": searched_total_articles,
            "articles": articles,
            "form": form,
            "article_page_ob": article_page_ob,
            "query": query
        }

# Get request is handled here.

    elif request.method == 'GET':

# Regex is applied to query term to process query term

        if query:
            pattern = r'(?i)\b' + query + r'\b'
            regex = re.compile(pattern)
            articles = []

# Articles are collected based on request

            articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
            for item in articl:
                articles.append(item)

            searched_total_articles = articl.count()

# Pagination is applied just in case

            paginated_articles = Paginator(articles, 10)
            page_number = request.GET.get('page', None)
            article_page_ob = paginated_articles.get_page(page_number)

            context = {
                "total_articles": total_articles,
                "searched_articles": searched_total_articles,
                "articles": articles,
                "form": form,
                "article_page_ob": article_page_ob,
                "query": query
            }

    return render(request, "articles_detail.html", context)