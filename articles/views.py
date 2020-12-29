import itertools
import json

from bson import json_util
from django.shortcuts import render
from .models import *
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://dbuserdolphin:dbpassworddolphin@cluster0.h6bhx.mongodb.net/dolphin?retryWrites=true&w=majority")
db = cluster["dolphin"]
collection = db["articles_article"]


def home(request):

    articles = article.objects.all()
    total_articles = articles.count()
    context = {"total_articles": total_articles}

    return render(request, "articles.html", context)

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
                    {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                              {"abstract": {"$regex": b, "$options": 'i'}},
                              {"abstract": {"$regex": c, "$options": 'i'}},
                              {"abstract": {"$regex": d, "$options": 'i'}}]},

                    {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                              {"title": {"$regex": b, "$options": 'i'}},
                              {"title": {"$regex": c, "$options": 'i'}},
                              {"title": {"$regex": d, "$options": 'i'}}]}
                ]
            }).limit(10)

            total_count = collection.count_documents({
                "$or": [
                    {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                              {"abstract": {"$regex": b, "$options": 'i'}},
                              {"abstract": {"$regex": c, "$options": 'i'}},
                              {"abstract": {"$regex": d, "$options": 'i'}}]},
                    {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                              {"title": {"$regex": b, "$options": 'i'}},
                              {"title": {"$regex": c, "$options": 'i'}},
                              {"title": {"$regex": d, "$options": 'i'}}]}
                ]
            })

            context["total_count_"+str(index)] = total_count
            if a != b and a != c and a != d:
                context["q_" + str(index)] = [a, b, c, d]

            if a == b and a == c and a == d:
                context["q_" + str(index)] = [a]

            if a == c and a == d and a != b:
                context["q_" + str(index)] = [a, b]

            if a == d and a != c:
                context["q_" + str(index)] = [a, b, c]


            for item in articles:
                my_array.append(item)

            context["articles_" + str(index)] = my_array
            request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
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
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                }).limit(10)

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
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
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                }).limit(10)

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
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
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                }).limit(10)

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
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
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                }).limit(10)

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
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
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},

                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                }).limit(10)

                total_count = collection.count_documents({
                    "$or": [
                        {"$and": [{"abstract": {"$regex": a, "$options": 'i'}},
                                  {"abstract": {"$regex": b, "$options": 'i'}},
                                  {"abstract": {"$regex": c, "$options": 'i'}},
                                  {"abstract": {"$regex": d, "$options": 'i'}}]},
                        {"$and": [{"title": {"$regex": a, "$options": 'i'}},
                                  {"title": {"$regex": b, "$options": 'i'}},
                                  {"title": {"$regex": c, "$options": 'i'}},
                                  {"title": {"$regex": d, "$options": 'i'}}]}
                    ]
                })

                context["total_count_" + str(index)] = total_count
                if a != b and a != c and a != d:
                    context["q_" + str(index)] = [a, b, c, d]

                if a == b and a == c and a == d:
                    context["q_" + str(index)] = [a]

                if a == c and a == d and a != b:
                    context["q_" + str(index)] = [a, b]

                if a == d and a != c:
                    context["q_" + str(index)] = [a, b, c]


                for item in articles:
                    my_array.append(item)

                context["articles_" + str(index)] = my_array
                request.session["articles_" + str(index)] = parse_json(context["articles_" + str(index)])
                index += 1


    return render(request, "dimension.html", {'context': context})


def parse_json(data):
    return json.loads(json_util.dumps(data))










