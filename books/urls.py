from django.urls import path

from books.views import BookView

urlpatterns = [
    path('', BookView.as_view())

]
