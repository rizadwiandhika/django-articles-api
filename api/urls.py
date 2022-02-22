
from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    # path('articles/<int:pk>/comments/', name='article_comments'),

    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    # path('articles/<int:pk>/', name='article_detail'),

    path('users/', views.users, name='users'),
    # path('articles/', name='articles'),

    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('', views.index, name='index'),
]
