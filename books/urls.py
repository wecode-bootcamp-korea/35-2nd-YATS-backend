from django.urls import path

from books.views import BookView, CancelView

urlpatterns = [
    path('', BookView.as_view()),
    path('/cancel', CancelView.as_view())

]
