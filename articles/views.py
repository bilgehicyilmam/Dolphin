from django.shortcuts import render
from .models import *
from .filters import ArticleFilter

def home(request):

    articles = article.objects.all()
    total_articles = articles.count()
    context = {"total_articles": total_articles}

    return render(request, "articles.html", context)










