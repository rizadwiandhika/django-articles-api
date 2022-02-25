from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.articles, name='articles'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('<int:pk>/comments/', views.article_comments, name='article_comments'),
    path('comments/', views.comments, name='comments'),
    path('comments/<int:pk>/', views.detail_comment, name='detail_comment'),
]
