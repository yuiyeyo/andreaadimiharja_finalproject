import random
from .models import Article

def featured_article(request):
    articles = Article.objects.all()
    featured = random.choice(articles) if articles.exists() else None
    return {"featured_article": featured}
