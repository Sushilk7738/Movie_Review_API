from django.contrib import admin
from .models import Movie, Review, Genre

admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Review)


