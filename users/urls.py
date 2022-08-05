from django.urls import path

from .views import KakaoCallBackView

urlpatterns = [
    path("/kakao", KakaoCallBackView.as_view())
]