
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('', views.users, name='users'),
]
