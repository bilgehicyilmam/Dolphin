from django.shortcuts import render
from .models import *


def home(request):

    articles = article.objects.all()

    return render(request, "articles.html", {'articles': articles})











