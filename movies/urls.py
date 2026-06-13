from django.urls import path
from . import views
urlpatterns = [
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/<int:pk>/', views.GenreDetailAPIView.as_view(), name='genre_detail'),
    

    path('movies/', views.MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', views.MovieDetailAPIView.as_view(), name='movie_detail'),
    

    path('reviews/', views.ReviewListView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', views.ReviewDetailAPIView.as_view(), name='review_detail'),
]
