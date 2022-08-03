import jwt

from django.conf import settings
from django.http import JsonResponse

from users import User

def login_decorator(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token,settings.SECRET_KEY, settings.ALGORITHM)
            user_id      = payload['user_id']
            request.user = User.objects.get(id=user_id)
            return func(self, request)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=400)
    return wrapper
