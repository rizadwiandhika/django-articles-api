from django.http import HttpRequest, Http404
from myproject.utils import success

def index(request: HttpRequest):
    if request.method != 'GET':
        raise Http404

    data = {
        'greeting': 'Welcome to Django Articles API!',
        'message': 'There are various endpoints available for this API which you can find in the API documentation',
        'api_documentation': 'https://descriptive-woodwind-387.notion.site/Django-Articles-API-a1d7a75f48d5437ca70e3d7d885b5159',
        'github_repo': 'https://github.com/rizadwiandhika/django-articles-api'
    }

    return success(data=data)