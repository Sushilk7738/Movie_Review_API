from django.shortcuts import render
from .models import Review, Movie, Genre
from .serializers import MovieWriteSerializer, ReviewSerializer, MovieSerializer, GenreSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .pagination import MoviePagination
from django.core.cache import cache
from rest_framework.throttling import AnonRateThrottle


class GenreListView(APIView):
    def get(self, request):
        search = request.query_params.get('search') 
        genres = Genre.objects.all()

        if search:
            genres = genres.filter(
                name__icontains=search
            )
        serializer = GenreSerializer(genres, many= True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenreSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class GenreDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Genre, pk=pk)

    def get(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def put(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
    def patch(self, request, pk):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre, data = request.data, partial = True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        genre = self.get_object(pk)
        genre.delete()
        return Response(
            {"message": "Genre deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT
        )




class MovieListView(APIView):
    
    throttle_classes = [AnonRateThrottle]
    def get(self, request):
        search = request.query_params.get('search')
        genre = request.query_params.get('genre')
        rating = request.query_params.get('rating')
        ordering = request.query_params.get('ordering')
        
        movies = Movie.objects.select_related('genre').order_by('id')

        if search:
            movies = movies.filter(
                title__icontains=search
            )

        if genre:
            movies = movies.filter(
                genre_id = genre
            )

        if rating:
            movies = movies.filter(
                rating = rating
            )
            
        if ordering:
            movies = movies.order_by(ordering)

        paginator = MoviePagination()
        
        paginated_movies = paginator.paginate_queryset(
            movies, 
            request
        )
            
        
        serializer = MovieSerializer(paginated_movies, many = True)
        return paginator.get_paginated_response(
            serializer.data
        )

    def post(self , request):
        serializer = MovieWriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(
            Movie.objects.select_related('genre'), 
            pk=pk
        )

    def get(self, request, pk):
        
        cache_key = f"movie_{pk}"

        movie_data = cache.get(cache_key)

        if movie_data is not None:
            print("Cache data found!")
            return Response(movie_data)
        
        print("Cache miss")
        movie = self.get_object(pk) 
        serializer = MovieSerializer(movie)
        
        cache.set(
            cache_key,
            serializer.data,
            timeout=60
        )
        
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieWriteSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete(f"movie_{pk}")
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        movie = self.get_object(pk)
        serializer = MovieWriteSerializer(movie, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            cache.delete(f"movie_{pk}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        cache.delete(f"movie_{pk}")
        return Response({"message": "movie deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    


class ReviewListView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ReviewDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Review, pk=pk)

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        review = self.get_object(pk)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


        