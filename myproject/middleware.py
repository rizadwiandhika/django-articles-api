import json

import jwt

from http import HTTPStatus

from django.http import HttpRequest
from django.core.cache import cache

from myproject.utils import error
from myproject import settings

def is_auth(methods=['POST', 'PUT', 'DELETE']):
    def wrapper(get_response):
        def middleware(request: HttpRequest, **kwargs: dict):
            if request.method in methods:
                token = request.headers.get('Authorization', None)
                if token is None or token == '':
                    return error(HTTPStatus.UNAUTHORIZED, 'Token is required')

                token = token.split(' ')[1]
                try:
                    decodedToken = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
                    tokenId = decodedToken.get('jti')
                    userId = decodedToken.get('data', {}).get('user_id', None)

                    userTokenBlacklist = json.loads(cache.get(userId, "[]"))
                    if tokenId in userTokenBlacklist:
                        raise Exception('Token is blacklisted')

                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception) as e:
                    print('jwt error:', e)
                    return error(HTTPStatus.UNAUTHORIZED, 'Invalid token')

                request.__setattr__('user', decodedToken)

            resp = get_response(request, **kwargs)
            return resp

        return middleware
    return wrapper

def parseJson(get_response):
    def middleware(request: HttpRequest, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError as e:
                print('error:', e)
                return error(HTTPStatus.BAD_REQUEST, e.msg)
        
            request.__setattr__('json', data)

        return get_response(request, **kwargs)
    return middleware