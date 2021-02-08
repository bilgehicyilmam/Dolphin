from django.test import SimpleTestCase
from articles.forms import *

class TestForms(SimpleTestCase):
    def test_article_search_valid_data(self):
        form = ArticleSearch(data={
            'abstract': 'article'
        })
        self.assertTrue(form.is_valid())

    def test_article_search_no_data(self):
        form = ArticleSearch(data={})
        self.assertTrue(form.is_valid())




# python manage.py test test.test_forms