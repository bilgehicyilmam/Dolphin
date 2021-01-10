from django.test import SimpleTestCase
from django.urls import reverse, resolve

from articles.views import *


class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse("home")
        self.assertEquals(resolve(url).func, home)

    def test_dimensional_search_url(self):
        url = reverse("dimensional_search")
        self.assertEquals(resolve(url).func, dimensional_search)



# python manage.py test test.test_url
