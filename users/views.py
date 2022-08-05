import requests
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User

class KakaoCallBackView(View):
    def get(self, request):
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        code = request.GET.get("code")

        data = {
            "grant_type"   : "authorization_code",
            "client_id"    : settings.KAKAO_REST_API_KEY,
            "redirect_uri" : settings.KAKAO_REDIRECT_URI,
            "client_secret": settings.KAKAO_SECRET_KEY,
            "code"         : code
        }

        response       = requests.post(kakao_token_api, data=data).json()
        access_token   = response['access_token']
        kakao_user_api = "https://kapi.kakao.com/v2/user/me"
        header         = {"Authorization": f"Bearer {access_token}"}
        user_info      = requests.get(kakao_user_api, headers=header).json()

        kakao_id       = user_info['id']
        kakao_email    = user_info['kakao_account']['email']
        kakao_nickname = user_info['properties']['nickname']

        user, is_created = User.objects.get_or_create(
            kakao_id = kakao_id,
            defaults = {
                "email"   : kakao_email,
                "nickname": kakao_nickname
            }
        )

        if not is_created:
            user.email    = kakao_email
            user.nickname = kakao_nickname
            user.save()

        status  = 201 if is_created else 200
        message = "FIRSTLOGIN" if is_created else "LOGIN"
        token   = jwt.encode({"id" : user.id}, settings.SECRET_KEY, settings.ALGORITHM)

        return JsonResponse({"message" : message, "token" : token}, status=status)
        






