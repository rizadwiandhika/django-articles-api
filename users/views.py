from http import HTTPStatus

from django.db import IntegrityError
from django.http import HttpRequest, Http404
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from myproject.middleware import parseJson, is_auth

from myproject.utils import success, error
from users.models import User

def index(request: HttpRequest):
    if request.method != 'GET':
        raise Http404

    message = "Welcome to articles API! This API is created using Django. You can explore the API by visiting the following links: "
    return success(HTTPStatus.OK, message)

@csrf_exempt
@is_auth(methods=['GET', 'PUT', 'DELETE'])
@parseJson
def users(request: HttpRequest):
    if request.method == 'GET':
        # usersModels = User.objects.all()
        # users = serializers.serialize('json', usersModels)
        # users = json.loads(users)
        users = list(User.objects.values()) # directly get every record as dictonary, not complex model

        # Don't return password
        for user in users:
            user.pop('password')

        return success(HTTPStatus.OK, data=users)

    if request.method == 'PUT':
        data = request.json
        userId = request.user.get('data', {}).get('user_id', None)
        payloadUserId = data.get('id', None)

        if userId is None or userId != payloadUserId:
            return error(HTTPStatus.UNAUTHORIZED, 'You are not authorized to perform this action')

        try:
            existingUser = User.objects.get(pk=userId)
        except User.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, 'User not found')

        existingUser.name = data.get('name', existingUser.name)

        try:
            existingUser.save()
        except IntegrityError as e:
            print(e)
            return error(HTTPStatus.INTERNAL_SERVER_ERROR, 'Something went wrong')
        
        return success(HTTPStatus.OK, 'User updated successfully')

@csrf_exempt
@is_auth(methods=['GET', 'DELETE'])
def user_detail(request, pk):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, 'User not found')

        user = model_to_dict(user)

        # Don't return password
        user.pop('password')


        return success(HTTPStatus.OK, data=user)

    if request.method == 'DELETE':
        userId = request.user.get('data', {}).get('user_id', None)

        if userId is None or userId != pk:
            return error(HTTPStatus.UNAUTHORIZED, 'You are not authorized to perform this action')

        try:
            existingUser = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return error(HTTPStatus.NOT_FOUND, 'User not found')

        try:
            existingUser.delete()
        except IntegrityError as e:
            print(e)
            return error(HTTPStatus.INTERNAL_SERVER_ERROR, 'Something went wrong')
        
        return success(HTTPStatus.OK, 'User deleted successfully')

    raise Http404
