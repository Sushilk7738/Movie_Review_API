from rest_framework import serializers
from .models import Movie, Review, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"
        

class MovieSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only = True)
    class Meta:
        model = Movie
        fields = '__all__'


class MovieWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError("Rating must be between 0 to 10")
        return value
    


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        
    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Stars must be between 1 to 5")
        return value


        