from django.urls import path

from stays.views import StayDetailView, EnterView

urlpatterns = [
    path('/<int:stay_id>', StayDetailView.as_view()),
    path('/<int:stay_id>', StayDetailView.as_view()),
    path('/entering', EnterView.as_view()),
]
