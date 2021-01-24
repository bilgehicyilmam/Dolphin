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

import datetime
import pycountry


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


    if 'q_0' in request.GET:
        query = request.GET["q_0"]
        queriess = query.split(" ")
        queries_0 = queries_0 + queriess

    if 'q_1' in request.GET:
        query = request.GET["q_1"]
        queriess = query.split(" ")
        queries_1 = queries_1 + queriess

    if 'q_2' in request.GET:
        query = request.GET["q_2"]
        queriess = query.split(" ")
        queries_2 = queries_2 + queriess

    return queries_0, queries_1, queries_2

def synonymous(query):

    synonymous_words = []

    for q in query:
        synonymous = sys_collection.find({"label": {"$regex": r'\b' + q + r'\b', "$options": 'i'}})
        for s in synonymous:
            for i in s["synonymous"]:
                synonymous_words.append(i)

    return synonymous_words

def dimensional_search(request):

    context = {}
    index = 0
    my_array = []

    if request.GET:

        queries_0, queries_1, queries_2 = reqs(request)

        queries_0_sys = synonymous(queries_0)
        queries_1_sys = synonymous(queries_1)
        queries_2_sys = synonymous(queries_2)

        print(queries_0_sys)
        print(queries_0)

        context["queries_0"] = queries_0
        context["queries_1"] = queries_1
        context["queries_2"] = queries_2


        if len(queries_0_sys) >= 1:

            for a in queries_0_sys:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a]
                index += 1
                my_array.clear()

        if len(queries_1_sys) >= 1:

            for b in queries_1_sys:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b]
                index += 1
                my_array.clear()

        if len(queries_2_sys) >= 1:

            for c in queries_2_sys:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + c + r'\b' + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [c]
                index += 1
                my_array.clear()

        for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

            if a is None and b is not None:
                a = b
            if a is None and c is not None:
                a = c
            if b is None and a is not None:
                b = a
            if c is None and a is not None:
                c = a


            articles = collection.find({
                "$or": [
                    {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                            ]},

                    {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                            ]}
                ]
            })

            if a != b and a != c:
                context["q_" + str(index)] = [a, b, c]
                request.session["q_" + str(index)] = [a, b, c]

            if a == b and a == c:
                context["q_" + str(index)] = [a]
                request.session["q_" + str(index)] = [a]

            if a == c and a != b:
                context["q_" + str(index)] = [a, b]
                request.session["q_" + str(index)] = [a, b]

            for item in articles:
                my_array.append(item)

            context["articles_" + str(index)] = my_array
            request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

            context["total_count_" + str(index)] = len(my_array)
            index += 1
            my_array.clear()

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              ]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                 ]}
                    ]
                })

                if a != b and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                if a == b and a == c:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                index += 1
                my_array.clear()

        if len(queries_2) > 1:

            queries_2.reverse()

            for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                ]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                               ]}
                    ]
                })

                if a != b and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                if a == b and a == c:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                index += 1
                my_array.clear()

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              ]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                ]}
                    ]
                })

                if a != b and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                if a == b and a == c:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                index += 1
                my_array.clear()

        for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

            if a is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a]
                index += 1
                my_array.clear()

            if b is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b]
                index += 1
                my_array.clear()

            if c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [c]
                index += 1
                my_array.clear()

            if a is not None and b is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, b]
                index += 1
                my_array.clear()

            if a is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, c]
                index += 1
                my_array.clear()

            if b is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b, c]
                index += 1
                my_array.clear()

        queries_1.reverse()
        queries_2.reverse()

        for (a, b, c) in itertools.zip_longest(queries_0, queries_1, queries_2):

            if a is not None and b is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, b]
                index += 1
                my_array.clear()

            if a is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [a, c]
                index += 1
                my_array.clear()

            if b is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b, c]
                index += 1
                my_array.clear()

        queries_1.reverse()

        for (b, c) in itertools.zip_longest(queries_1, queries_2):

            if b is not None and c is not None:

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}}]}
                    ]
                })

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])

                context["total_count_" + str(index)] = len(my_array)
                context["q_" + str(index)] = [b, c]
                index += 1
                my_array.clear()


    return render(request, "dimension.html", {'context': context})


def parse_json(data):
    return json.loads(json_util.dumps(data))


def split_line(query):
    # split the text
    result = query.split(",")
    words = []
    # for each word in the line:
    for word in result:
        # append the word
        words.append(word)
    return words

# def split_space(queris):
#     # split the text
#     result = queris.split(" ")
#     words = []
#     # for each word in the term:
#     for word in result:
#         # append the word
#         words.append(word)
#     return words


def home(request):
    all_articles = article.objects.all()
    form = ArticleSearch()
    total_articles = all_articles.count()
    context = {
        "total_articles": total_articles,
        "form": form,
    }
    query = request.GET.get('abstract', '')
    print(query)
    date = request.GET.get('publication_date', '')
    date2 = request.GET.get('publication_date', '')
    print(date)
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
    elif request.method == 'GET':

        if query:
            queris = split_line(query)
            print(queris)
            articles = []
            counter = 0
            for que in queris:
                counter+= 1
                print(counter)
                pat = r'(?i)\b(?:(?!\band\b|\bor\b|\bbut\b)\w)+\b'
                #reg = re.compile(pat)
                que = re.findall(pat, que)
                print(que)
                pp = r'(?i)'
                for qu in que:
                    pt = r'\b' + qu + r'\b\W+(?:\w+\W+){0,4}?'
                    tmp= pp + pt
                    pp= tmp
                    #pt = str(pattern)
                print(pp)
                regex = re.compile(pp)
                articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
                #articl = collection.find({"$and": [{"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]}, {"publication_date": {date}}]})
                if len(articles) == 0 and counter == 1:
                    for item in articl:
                        articles.append(item)
                else:
                    temp_arc=[]
                    for a in articl:
                        if a in articles:
                            temp_arc.append(a)
                    articles = temp_arc

            searched_total_articles = len(articles)

            paginated_articles = Paginator(articles, 10)
            page_number = request.GET.get('page', None)
            article_page_ob = paginated_articles.get_page(page_number)
            for item in paginated_articles.object_list:
                authors = item['authors']
                keywords = item['keywords']
                b = json.loads(authors)
                c = json.loads(keywords)
                item['authors'] = b
                item['keywords'] = c
            #pprint (vars(paginated_articles))
            context = {
                "total_articles": total_articles,
                "searched_articles": searched_total_articles,
                "articles": articles,
                "form": form,
                "article_page_ob": article_page_ob,
                "query": query,
                "queris": queris
            }

    return render(request, "articles.html", context)


def article_detail(request, pubmed_id):
    all_articles = article.objects.all()
    form = ArticleSearch(request.POST or None)
    total_articles = all_articles.count()
    #pubmed_id = str(pubmed_id)
    # f= str(pubmed_id)
    # e= len(f)
    # pid= pubmed_id.to_bytes(e, "little")
    # pickle.dumps(pid)
    # d=pickle.loads(pid)
    # pubmed_id=d
    #pidd= str(pubmed_id)
    detail_article = article.objects.get(pubmed_id = pubmed_id)
    print(detail_article)
    #detail_article = collection.find_one({"pubmed_id": {pubmed_id}})
    # for item in detail_article.object_list:
    #     pid = item['pubmed_id']
    #     d = pickle.loads(pid)
    #     item['pubmed_id'] = d
    #import pprint
    #pprint.pprint(vars(detail_article))
    idd = detail_article.id
    tit = detail_article.title
    abst = detail_article.abstract
    #pid= detail_article['pubmed_id']
    keyw = detail_article.keywords
    jour = detail_article.journal
    pub_date = detail_article.publication_date
    auth = detail_article.authors
    conc= detail_article.conclusions
    res= detail_article.results
    copy = detail_article.copyrights
    dooi = detail_article.doi
    context = {
        # "total_articles": total_articles,
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
    elif request.method == 'GET':

        if query:
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

    return render(request, "articles_detail.html", context)