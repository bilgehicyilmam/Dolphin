from django.urls import path
from . import views
from .views import home

urlpatterns = [

   path('', views.home, name='home'),
   path('articles_detail/', views.article_detail, name='articles_detail'),
   #path('', views.search, name='search'),
   path('dimsearch/', views.dimensional_search, name='dimensional_search'),
   path('all_articles/', views.all_articles, name='all_articles'),
   path('chart/', views.chart, name='chart'),
]
