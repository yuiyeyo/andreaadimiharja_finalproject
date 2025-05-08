import random
from django.shortcuts import render, get_object_or_404
from .models import VisualContent
from .models import Article, Comment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .forms import ArticleForm
import csv
from django.http import JsonResponse
import os
from django.conf import settings
from django.http import JsonResponse
from .forms import AdvertisementForm
from .models import Advertisement
from django.contrib.admin.views.decorators import staff_member_required
from difflib import get_close_matches
from .forms import SearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import requests
from django.db.models import Q
import operator
from functools import reduce
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Notification, Article, Profile, Creator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.paginator import EmptyPage
from .models import Notification, Profile

@login_required
def toggle_favorite_creators(request, creator_id):
    profile = request.user.profile  
    try:
        creator_user = User.objects.get(pk=creator_id)
        if creator_user == request.user:
            return HttpResponse("You cannot favorite yourself.", status=400)

        if creator_user in profile.favorite_creators.all():
            profile.favorite_creators.remove(creator_user)
        else:
            profile.favorite_creators.add(creator_user)
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    except User.DoesNotExist:
        return HttpResponse("Creator not found.", status=404)



def feed_api(request):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(Article.objects.all().order_by('article_id'), 10)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({"articles": [], "has_next": False})

    articles = [
        {
            "id": article.article_id,
            "headline": article.headline,
            "image_url": article.image_url or '',
        }
        for article in page_obj
    ]
    return JsonResponse({
        "articles": articles,
        "has_next": page_obj.has_next()
    })


def feed(request):
    articles = Article.objects.order_by('article_id')
    paginator = Paginator(articles, 10)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        articles_data = []
        for article in page_obj:
            articles_data.append({
                'id': article.article_id,
                'headline': article.headline,
                'image_url': article.get_image_url(),
            })
        
        return JsonResponse({
            'articles': articles_data,
            'has_next': page_obj.has_next()
        })

    return render(request, 'feed.html', {'page_obj': page_obj})


@login_required
def manage_alerts(request):
    alerts = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'alerts': alerts})
#def manage_alerts(request):
#    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#    if request.method == 'POST':
#        notifications.update(is_read=True)
#        return redirect('manage_alerts')
#    return render(request, 'manage_alerts.html', {'notifications': notifications})


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

#@login_required
#def notifications_page(request):
#    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
def favorite_editor(request, editor_id):
    profile = request.user.profile
    editor = get_object_or_404(Profile, id=editor_id)
    if editor not in profile.favorite_editors.all():
        profile.favorite_editors.add(editor)
    else:
        profile.favorite_editors.remove(editor)
    return redirect('home')



@login_required
def feed_articles(request):
    offset = int(request.GET.get('offset', 0))
    limit = 10
    articles = Article.objects.all().order_by('-created_at')[offset:offset+limit]
    data = [
        {'id': article.id, 'headline': article.headline, 'content': article.content[:150]}
        for article in articles
    ]
    return JsonResponse({'articles': data})

def recommended_articles(article):
    """ Logic for recommending articles at the bottom of each article page """
    keywords = article.content.split()[:5] 
    recommendations = Article.objects.filter(content__icontains=keywords[0]).exclude(id=article.id)[:3]
    return recommendations



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        country = request.POST.get('country')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return redirect('login')

    countries = []
    try:
        response = requests.get('https://restcountries.com/v3.1/all')
        if response.status_code == 200:
            countries = sorted([c['name']['common'] for c in response.json()])
    except:
        countries = []

    return render(request, 'register.html', {'countries': countries})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            send_mail(
                subject='Password Reset Request',
                message='Please visit our support to reset your password.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return render(request, 'forgot_password.html', {'message': 'Email sent if account exists.'})
    return render(request, 'forgot_password.html')

def search_articles(request):
    form = SearchForm(request.GET or None)
    query = request.GET.get('query')
    articles = Article.objects.all()
    results = []
    suggestions = []

    if query:
        results = articles.filter(headline__icontains=query)
        if not results.exists():
            suggestions = articles[:3]  

    return render(request, 'search_results.html', {
        'form': form,
        'articles': results,
        'suggestions': suggestions
    })


@staff_member_required
def submit_advertisement(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AdvertisementForm()
    return render(request, "submit_advertisement.html", {"form": form})



@staff_member_required
def edit_article(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'edit_article.html', {'form': form})

@staff_member_required
def delete_article(request, id):
    article = get_object_or_404(Article, pk=id)
    article.delete()
    return redirect('home')


def articles_api(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'articles.csv')
    articles = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            articles.append(row)

    return JsonResponse({'articles': articles})


@login_required
def submit_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.save()
            form.save_m2m()

            favoriting_profiles = Profile.objects.filter(favorite_creators=request.user)
            for profile in favoriting_profiles:
                if profile.notify_setting in ["daily", "immediate"]:
                    Notification.objects.create(
                        user=profile.user,
                        message=f"{request.user.username} just posted a new article: {article.headline}"
                    )

            return redirect('article_detail', id=article.article_id)
    else:
        form = ArticleForm() 

    return render(request, 'submit_article.html', {'form': form})


#def submit_article(request):
#    if request.method == "POST":
#        form = ArticleForm(request.POST, request.FILES)
#        if form.is_valid():
#            article = form.save(commit=False)
#            article.creator = request.user 
#            article.save() 
            #form.save()
            #for user in Profile.objects.all():
            #    if any(sub in article.content for sub in user.subscriptions):
            #        if user.notify_setting in ['all', 'subscription']:
            #            Notification.objects.create(user=user.user, message=f"New article about {sub}!")

#            return redirect("home") 
#    else:
#        form = ArticleForm()
#
#    return render(request, "submit_article.html", {"form": form})



@csrf_exempt
def like_article(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)
    article.likes += 1
    article.save()
    return JsonResponse({'likes': article.likes})

@csrf_exempt
@login_required
@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, article_id=article_id)

    if request.method == "POST":
        content = request.POST.get("text", "").strip()
        comment = Comment.objects.create(name=request.user.username, article=article, text=content)

        if article.creator != request.user:
            Notification.objects.create(
                user=article.creator,
                message=f"{request.user.username} commented on your article '{article.headline}'"
            )

        return redirect('article_detail', id=article.article_id)

#def add_comment(request, article_id):
#    if request.method == "POST":
#        article = get_object_or_404(Article, pk=article_id)#
#
#        comment_text = request.POST.get("text", "").strip()
#
#        if comment_text:
#            comment = Comment.objects.create(
#                article=article,
#                name=request.user.username,
#                text=comment_text
#            )
#
#            if hasattr(article, 'author') and request.user.username != article.author.username:
#                Notification.objects.create(
#                    user=article.author,
#                    message=f"{request.user.username} commented on your article: '{article.headline}'"
#                )
#
#            return JsonResponse({
#                "message": "Comment added!",
#                "name": comment.name,
#                "text": comment.text,
#                "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
#            })
#
#    return JsonResponse({"error": "Invalid request"}, status=400)
    
#def add_comment(request, article_id):
#    if request.method == "POST":
#        article = get_object_or_404(Article, pk=article_id)  # Should be pk, not article_id
#
#        comment_text = request.POST.get("text", "").strip()
#
#        if comment_text:
#            comment = Comment.objects.create(
#                article=article,
#                name=request.user.username,  # Always use logged-in user's username
#                text=comment_text
#            )
#            return JsonResponse({
#                "message": "Comment added!",
#                "name": comment.name,
#                "text": comment.text,
#                "created_at": comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
#            })
#
#    return JsonResponse({"error": "Invalid request"}, status=400)

def base(request):
    articles = Article.objects.all()  
    featured_article = random.choice(articles) if articles else None  
    return render(request, "home.html", {"featured_article": featured_article})


def search(request):
    query = request.GET.get("query", "").strip()  
    articles = Article.objects.filter(headline__icontains=query) if query else []  
    return render(request, "search_results.html", {"query": query, "articles": articles})


#def article_detail(request, id):
#    article = get_object_or_404(Article, article_id=id)  # Ensure `article_id` is correct
#    return render(request, "article.html", {"article": article})  # Use "article.html"

#def article_detail(request, id):
#    article = get_object_or_404(Article, article_id=id)
#    related_articles = Article.objects.exclude(article_id=id)[:3]  
#
#    return render(request, "article.html", {
#        "article": article,
#        "articles": related_articles,  
#    })

from django.contrib.auth.models import AnonymousUser

def article_detail(request, id):
    article = get_object_or_404(Article, pk=id)
    related_articles = Article.objects.exclude(article_id=id)[:3] 
    recommended = Article.objects.filter(
        Q(pokemon=article.pokemon) |
        Q(city=article.city)
    ).exclude(pk=article.pk)[:3]

    profile = None

    if request.user.is_authenticated:
        if not hasattr(request.user, 'profile'):
            profile = Profile.objects.create(user=request.user)
        else:
            profile = request.user.profile

        keywords = article.content.lower().split()
        for word in keywords:
            if word in profile.interests:
                continue
            request.session.setdefault('read_keywords', {})
            request.session['read_keywords'][word] = request.session['read_keywords'].get(word, 0) + 1
            if request.session['read_keywords'][word] >= 3:
                profile.interests.append(word)
                profile.save()

    return render(request, 'article.html', {
        'article': article,
        'profile': profile,
        'recommended': recommended
    })




def home(request):
    articles = Article.objects.all()
    highlight_article = random.choice(articles) if articles else None
    return render(request, "home.html", {
        'articles': articles,
        'highlight_article': highlight_article,
    })

#def home(request):
#    articles = Article.objects.all()
#    print(articles)  # Add this line to check if articles are being fetched correctly
#    return render(request, "home.html", {"articles": articles})



