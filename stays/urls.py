from django.urls import path

from stays.views import StayDetailView, RoomDetailView, FindStayView

urlpatterns = [
    path('findstay/<int:stay_id>', StayDetailView.as_view()),
    path('room/<str:room_name>', RoomDetailView.as_view()),
    path('findstay', FindStayView.as_view()),
]
