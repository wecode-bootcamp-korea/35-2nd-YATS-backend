from django.urls import path, include

urlpatterns = [
    path('likes', include('likes.urls')),
    path('books', include('books.urls')),
    path('findstay', include('stays.urls')), 
]