from articles.models import article

article.objects.filter(name__contains='epidemic')
