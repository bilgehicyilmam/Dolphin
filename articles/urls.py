from django.urls import path
from . import views
from .views import home

urlpatterns = [

   path('', views.home, name='home'),
   path('articles_detail/<int:pubmed_id>', views.article_detail, name='articles_detail'),
   path('dimsearch/', views.dimensional_search, name='dimensional_search'),

]
