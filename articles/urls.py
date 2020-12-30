from django.urls import path
from . import views

urlpatterns = [

   path('', views.home, name='home'),
   path('dimsearch/', views.dimensional_search, name='dimensional_search'),
   path('all_articles/', views.all_articles, name='all_articles'),
]
