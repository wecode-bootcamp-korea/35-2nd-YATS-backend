from django.urls import path, include

urlpatterns = [
    path('likes', include('likes.urls')),
    path('books', include('books.urls')),
    path('', include('stays.urls')), 
    path("users", include("users.urls"))
]
