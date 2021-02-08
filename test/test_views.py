from django.test import Client, TestCase
from django.urls import reverse
import unittest
from pymongo import MongoClient
from articles.models import *
import json


cluster = MongoClient("mongodb+srv://dbuserdolphin:dbpassworddolphin@cluster0.h6bhx.mongodb.net/dolphin?retryWrites=true&w=majority")
db = cluster["dolphin"]
collection = db["articles_article"]


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_GET(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)
        #search_result = self.client.get(reverse("home", args=[json.dumps({'abstract': 'amygdala'})]))


    def test_dimensional_search_GET(self):
        response = self.client.get(reverse("dimensional_search"))
        self.assertEquals(response.status_code, 200)

        #mn = collection.count_documents({"abstract": {"$regex": "amygdala", "$options": 'i'}})
        #self.assertEquals(3, mn)


    def test_article_detail_GET(self):
        response = self.client.get(reverse("articles_detail", args=["32840758"]))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.context['pubmed_id'], 32840758)
        self.assertEqual(response.context['tit'], "SARS-CoV-2 Infectivity and Neurological Targets in the Brain.")



# python manage.py test test.test_views