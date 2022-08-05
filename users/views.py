import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User
from core.utils   import KakaoAPI


class KakaoCallBackView(View):
    def get(self, request):
        code = request.GET.get("code")

        kakao_api = KakaoAPI(
                        settings.KAKAO_REST_API_KEY, 
                        settings.KAKAO_REDIRECT_URI, 
                        settings.KAKAO_SECRET_KEY
                        )

        kakao_token     = kakao_api.get_token(code)
        kakao_user_info = kakao_api.get_user_info(kakao_token)

        kakao_id       = kakao_user_info['id']
        kakao_email    = kakao_user_info['kakao_account']['email']
        kakao_nickname = kakao_user_info['properties']['nickname']

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
        






