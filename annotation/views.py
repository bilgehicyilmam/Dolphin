from django.shortcuts import render

# Create your views here.
from articles.models import article

def annot(request):

    articles = article.objects.filter(abstract__contains='amygdala') | article.objects.filter(title__contains='amygdala')
    for e in articles:
        print(e.id)

    total_articles = articles.count()
    context = {"total_articles": total_articles}


    return render(request, "annotation.html", context)
