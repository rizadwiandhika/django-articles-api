import bcrypt
import jwt

from http import HTTPStatus
from datetime import datetime, timedelta

from django.db import IntegrityError
from django.http import HttpRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from myproject import settings
from myproject.middleware import parseJson
from myproject.utils import success, error

from users.models import User

@csrf_exempt
@parseJson
def register(request: HttpRequest):
    if request.method != 'POST':
        raise Http404

    data = request.json

    email = data.get('email', None)
    name = data.get('name', None)
    password = data.get('password', None)

    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        user = User.objects.create(email=email, name=name, password=password)
    except IntegrityError as e:
        return error(HTTPStatus.BAD_REQUEST, e.__cause__.__str__())

    # user = serializers.serialize('json', [user,])
    # user = json.loads(new_user)[0]
    user = model_to_dict(user)
    user.pop('password')
    
    return success(HTTPStatus.CREATED, 'User created successfully.', data=user)

@csrf_exempt
@parseJson
def login(request: HttpRequest):
    if request.method != 'POST':
        raise Http404

    email = request.json.get('email', '')
    password = request.json.get('password', '')

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return error(HTTPStatus.NOT_FOUND, 'User not found.')

    doesMatch = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if not doesMatch:
        return error(HTTPStatus.UNAUTHORIZED, 'Invalid password.')
    

    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {'exp': expire, 'data': {'user_id': user.id, 'email': user.email}}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

    return success(HTTPStatus.OK, 'Login success.', {'token': token})