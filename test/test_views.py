from django.test import Client
from django.urls import reverse
import unittest
from pymongo import MongoClient



cluster = MongoClient("mongodb+srv://dbuserdolphin:dbpassworddolphin@cluster0.h6bhx.mongodb.net/dolphin?retryWrites=true&w=majority")
db = cluster["dolphin"]
collection = db["articles_article"]


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_GET(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)

    def test_dimensional_search_GET(self):
        response = self.client.get(reverse("dimensional_search"))
        self.assertEquals(response.status_code, 200)
        mn = collection.count_documents({"abstract": {"$regex": "amygdala", "$options": 'i'}})
        self.assertEquals(3, mn)







# python manage.py test test.test_views