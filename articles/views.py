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


def home(request):

    articles = article.objects.all()
    total_articles = articles.count()
    context = {"total_articles": total_articles}
    return render(request, "articles.html", context)

import datetime

def all_articles(request):

    context = {}
    for i in range(30):
        context["articles_"+str(i)] = request.session.get("articles_"+str(i))
        context["q_"+str(i)] = request.session.get("q_"+str(i))
        context["total_count_"+str(i)] = request.session.get("total_count_"+str(i))



    for i in range(30):
        dates = []
        articles = {}
        thearticles = context["articles_" + str(i)]
        if thearticles is not None:
            for item in thearticles:
                date = item["publication_date"]
                date = list(date.values())[0]
                s = str(date)
                date = int(s[:10])
                date = datetime.datetime.fromtimestamp(date).strftime("%Y, %B")
                dates.append(date)
                if date in articles.keys():
                    articles[date].append(item)
                else:
                    articles[date] = []
                    articles[date].append(item)

            context["articles" + str(i)] = articles
            label = {i: dates.count(i) for i in dates}
            context["labels_" + str(i)] = list(label.keys())
            context["counts_" + str(i)] = list(label.values())

    return render(request, "all_articles.html", context)


def reqs(request):

    queries_0 = []
    queries_1 = []
    queries_2 = []
    queries_3 = []

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

    if 'q_3' in request.GET:
        query = request.GET["q_3"]
        queriess = query.split(" ")
        queries_3 = queries_3 + queriess

    return queries_0, queries_1, queries_2, queries_3


def dimensional_search(request):

    context = {}
    index = 0
    my_array = []

    if request.GET:

        queries_0, queries_1, queries_2, queries_3 = reqs(request)

        context["queries_0"] = queries_0
        context["queries_1"] = queries_1
        context["queries_2"] = queries_2
        context["queries_3"] = queries_3

        for (a, b, c, d) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3):

            if a is None and b is not None:
                a = b
            if a is None and c is not None:
                a = c
            if b is None and a is not None:
                b = a
            if c is None and a is not None:
                c = a
            if d is None and a is not None:
                d = a

            articles = collection.find({
                "$or": [
                    {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},

                    {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                ]
            })

            total_count = collection.count_documents({
                "$or": [
                    {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},
                    {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                              {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                ]
            })

            context["total_count_"+str(index)] = total_count
            request.session["total_count_"+str(index)] = total_count
            if a != b and a != c and a != d:
                context["q_" + str(index)] = [a, b, c, d]
                request.session["q_" + str(index)] = [a, b, c, d]

            if a == b and a == c and a == d:
                context["q_" + str(index)] = [a]
                request.session["q_" + str(index)] = [a]

            if a == c and a == d and a != b:
                context["q_" + str(index)] = [a, b]
                request.session["q_" + str(index)] = [a, b]

            if a == d and a != c:
                context["q_" + str(index)] = [a, b, c]
                request.session["q_" + str(index)] = [a, b, c]


            for item in articles:
                my_array.append(item)

            context["articles_" + str(index)] = my_array
            request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
            my_array.clear()
            index += 1

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c, d) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a
                if d is None and a is not None:
                    d = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]
                    request.session["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
                my_array.clear()
                index += 1

        if len(queries_2) > 1:

            queries_2.reverse()

            for (a, b, c, d) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a
                if d is None and a is not None:
                    d = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]
                    request.session["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
                my_array.clear()
                index += 1

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c, d) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a
                if d is None and a is not None:
                    d = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]
                    request.session["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
                my_array.clear()
                index += 1


        if len(queries_3) > 1:

            queries_3.reverse()

            for (a, b, c, d) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a
                if d is None and a is not None:
                    d = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]
                    request.session["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
                my_array.clear()
                index += 1

        if len(queries_1) > 1:

            queries_1.reverse()

            for (a, b, c, d) in itertools.zip_longest(queries_0, queries_1, queries_2, queries_3):

                if a is None and b is not None:
                    a = b
                if a is None and c is not None:
                    a = c
                if b is None and a is not None:
                    b = a
                if c is None and a is not None:
                    c = a
                if d is None and a is not None:
                    d = a

                articles = collection.find({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"abstract": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": r'\b' + a + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + b + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + c + r'\b', "$options": 'i'}},
                                  {"title": {"$regex": r'\b' + d + r'\b', "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]
                    request.session["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]
                    request.session["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]
                    request.session["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]
                    request.session["q_" + str(index)] = [a, b, c]

                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
                my_array.clear()
                index += 1

    return render(request, "dimension.html", {'context': context})


def parse_json(data):
    return json.loads(json_util.dumps(data))

import datetime


def chart(request):

    context = {}
    for i in range(30):
        context["articles_"+str(i)] = request.session.get("articles_"+str(i))

    data = []
    labels = []


    for i in range(2):

        dates = []
        context["thearticles_" + str(i)] = context["articles_" + str(i)]
        for item in context["articles_" + str(i)]:
            date = item["publication_date"]
            year = date.year
            month = date.month
            the_date = str(year) + ", " + str(month)
            dates.append(the_date)

        my_dict = {i: dates.count(i) for i in dates}
        context.labels = labels

        context["all_" + str(i)] = my_dict

    return render(request, "chart.html", context)

def split_line(query):
    # split the text
    result = query.split(" ")
    words = []
    # for each word in the line:
    for word in result:
        # append the word
        words.append(word)
    return words


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
            articles = []
            for q in queris:
                pattern = r'(?i)\b' + q + r'\b'
                regex = re.compile(pattern)
                articl = collection.find({"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]})
                #articl = collection.find({"$and": [{"$or": [{"abstract": {"$regex": regex}}, {"title": {"$regex": regex}}]}, {"publication_date": {date}}]})
                if len(articles) == 0:
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


def article_detail(request):
    all_articles = article.objects.all()
    form = ArticleSearch(request.POST or None)
    total_articles = all_articles.count()
    context = {
        "total_articles": total_articles,
        "form": form,
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

    return render(request, "articles_detail.html", )







