from django.db import models


# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, primary_key=True)


class Director(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    box_office_collection_in_crores = models.FloatField()
    director = models.ForeignKey(Director, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.movie_id


class Actor(models.Model):
    actor_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.ForeignKey(Gender, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.actor_id


class Cast(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    is_debut_movie = models.BooleanField(default=False)


class Rating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='rating')
    rating_one_count = models.PositiveIntegerField(default=0)
    rating_two_count = models.PositiveIntegerField(default=0)
    rating_three_count = models.PositiveIntegerField(default=0)
    rating_four_count = models.PositiveIntegerField(default=0)
    rating_five_count = models.PositiveIntegerField(default=0)
