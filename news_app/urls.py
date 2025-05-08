from django.urls import path
from . import views
from .views import like_article
from .views import submit_article
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path("", views.home, name="home"),
    path("articles/<int:id>/", views.article_detail, name="article_detail"),
    path('search/', views.search_articles, name='search_articles'),
    path('like/<int:article_id>/', like_article, name='like_article'),
    path("articles/<int:article_id>/comment/", views.add_comment, name="add_comment"),
    path("submit/", submit_article, name="submit_article"),
    path('api/articles/', views.articles_api, name='articles_api'),
    path('delete_article/<int:id>/', views.delete_article, name='delete_article'),
    path('api/article/<int:id>/', views.articles_api, name='article_detail_api'),
    path("submit_advertisement/", views.submit_advertisement, name="submit_advertisement"),
    path("edit_article/<int:id>/", views.edit_article, name="edit_article"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('notifications/', views.manage_alerts, name='manage_alerts'),
    path('favorite_editor/<int:editor_id>/', views.favorite_editor, name='favorite_editor'),
    path("", views.feed, name="home"),
    path('feed_api/', views.feed_api, name='feed_api'),
    path('toggle_favorite/<int:creator_id>/', views.toggle_favorite_creators, name='toggle_favorite_creators'),
]

if settings.DEBUG:
    urlpatterns += static(settings.DATA_URL, document_root=settings.DATA_ROOT)
