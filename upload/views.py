from http import HTTPStatus

from django.http import Http404, HttpRequest
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from myproject import settings

from myproject.utils import success, error

from .utils import is_valid_image, generate_filename

@csrf_exempt
def upload_image(request: HttpRequest):
    if request.method != 'POST':
        raise Http404

    thumbnail = request.FILES['thumbnail']

    if not thumbnail:
        return error(HTTPStatus.BAD_REQUEST, 'Thumbnail is required')
    
    if not is_valid_image(thumbnail):
        return error(HTTPStatus.BAD_REQUEST, 'File can only be an image with the following extensions: jpg, jpeg, png')

    fs = FileSystemStorage()
    filename = fs.save(generate_filename(thumbnail.name), thumbnail)
    url = fs.url(filename)
    return success(HTTPStatus.OK, data={'url': settings.DOMAIN + url})