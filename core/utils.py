import jwt, requests

from django.conf import settings
from django.http import JsonResponse

from users.models import User

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

class KakaoAPI:
    def __init__(self, client_id, redirect_uri, client_secret):
        self.client_id     = client_id
        self.redirect_uri  = redirect_uri
        self.client_secret = client_secret

    def get_token(self, auth_code):
        url = "https://kauth.kakao.com/oauth/token"

        data = {
            "grant_type"   : "authorization_code",
            "client_id"    : self.client_id,
            "redirect_uri" : self.redirect_uri,
            "client_secret": self.client_secret,
            "code"         : auth_code
        }

        response       = requests.post(url, data=data).json()
        access_token   = response['access_token']

        return access_token

    def get_user_info(self, token):
        url       = "https://kapi.kakao.com/v2/user/me"
        header    = {"Authorization": f"Bearer {token}"}
        user_info = requests.get(url, headers=header).json()

        return user_info