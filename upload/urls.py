from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
    path('', views.upload_image, name='upload_image'),
]
