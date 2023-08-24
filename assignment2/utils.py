from .models import Cast,Movie,Director, Actor, Rating
from django.db.models import Avg, Count
from django.core.exceptions import ObjectDoesNotExist


def get_no_of_distinct_movies_actor_acted(actor_id):
    movie_count = Cast.objects.filter(actor=actor_id).values('movie').aggregate(movie_count=Count('actor'))
    return movie_count['movie_count']


def get_movies_directed_by_director(director_obj):
    all_movies_query = Movie.objects.filter(director = director_obj)
    all_movies_list = list(all_movies_query)
    return all_movies_list


def get_average_rating_of_movie(movie_obj):
    try:
        ratings = Rating.objects.get(movie = movie_obj.movie_id)
        rating = 0
        rating += ratings.rating_one_count
        rating += ratings.rating_two_count
        rating += ratings.rating_three_count
        rating += ratings.rating_four_count
        rating += ratings.rating_five_count
        return rating
    except ObjectDoesNotExist:
        return 0


def delete_movie_rating(movie_obj):
    try:
        rating_obj = Rating.objects.get(movie=movie_obj.movie_id)
        rating_obj.delete()
        return "Deleted Succesfully"
    except ObjectDoesNotExist:
        return "Object Doesnt Exists"


def get_all_actor_objects_acted_in_given_movies(movie_objs):
    query = list(Cast.objects.filter(movie__in=movie_objs).values_list('actor').distinct())
    return query


def update_director_for_given_movie(movie_obj, director_obj):
    movie_obj.director = director_obj.name
    movie_obj.save()
    return "Updated Succesfully"


def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    query = list(Cast.objects.filter(actor__name__istartswith = "hari").values_list('movie').distinct())
    return query


def remove_all_actors_from_given_movie(movie_obj):
    movie_obj.cast_set.all().delete()
    return movie_obj.cast_set.all()


def get_all_rating_objects_for_given_movies(movie_objs):
    query = list(Rating.objects.filter(movie__movie_id__in = movie_objs))
    return query