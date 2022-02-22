from django.http import JsonResponse

def success(status=200, message="Success", data = None): 
    payload = {
        'meta': {
            'code': status,
            'message': message
        },
        'data': data
    }

    if data is None:
        del payload['data']

    return JsonResponse(payload, status=status)

def error(status = 500, message = ""):
    payload = {
        'error': {
            'code': status,
            'message': message
        }
    }
    return JsonResponse(payload, status=status)