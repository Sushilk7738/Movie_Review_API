from django.db import models



class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateTimeField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.title} - {self.genre}"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, name='reviews')
    reviewer_name = models.CharField(max_length=100, default='Unknown')
    comment = models.TextField()
    stars = models.IntegerField()

    def __str__(self):
        return self.reviewer_name
    

