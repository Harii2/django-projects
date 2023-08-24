from django.db.models import Q, Avg, Sum, Count, Case, When
from .models import Actor, Movie, Cast, Director, Rating
from django.db import models
from assignment3.utils import get_movies_by_given_movie_names


def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    # Firstly creating Directors objects
    directors_instances = []
    for director in directors_list:
        directors_instances.append(Director(name=director))

    # Actors_instances
    actors_instances = []
    for actor in actors_list:
        actor_obj = Movie(actor_id=actor['actor_id'], name=actor['actor_name'], gender=actor['gender'])
        actors_instances.append(actor_obj)

    # movies_list and cast instances
    movies_instances = []
    cast_instances = []
    for movie in movies_list:
        movie_obj = Movie(movie_id=movie['movie_id'], name=movie['name'], director=movie['director_name'],
                          box_office_collection_in_crores=movie['box_office_collection_in_crores'],
                          release_date=movie['release_date'])
        movies_instances.append(movie_obj)
        for actor in movie['actors']:
            cast_obj = Cast(movie=movie['movie_id'], actor=actor['actor_id'], role=actor['role'],
                            is_debut_movie=actor['is_debut_movie'])
            cast_instances.append(cast_obj)

    ratings_instances = []
    for rating in movie_rating_list:
        rating_obj = Rating(movie=rating['movie_id'],
                            rating_one_count=rating['rating_one_count'],
                            rating_two_count=rating['rating_two_count'],
                            rating_three_count=rating['rating_three_count'],
                            ratig_four_count=rating['rating_four_count'],
                            rating_five_count=rating['rating_five_count']
                            )
        ratings_instances.append(rating_obj)

    try:
        Director.objects.bulk_create(directors_instances)
        Actor.objects.bulk_create(actors_instances)
        Movie.objects.bulk_create(movies_instances)
        Cast.objects.bulk_create(cast_instances)
        Rating.objects.bulk_create(ratings_instances)
    except Exception as e:
        return e


def remove_all_actors_from_given_movie(movie_object):
    all_actors_from_given_movie = Cast.objects.filter(movie=movie_object.movie_id)
    all_actors_from_given_movie.delete()
    return f"Deleted Succesfully for the given movie {movie_object.movie_id}"


def get_all_rating_objects_for_given_movies(movie_objs):
    all_rating_objects_for_given_movies = list(Rating.objects.filter(movie__movie_id__in=movie_objs))
    return all_rating_objects_for_given_movies


def get_movies_by_given_movie_names(movie_names):
    q = Q()
    for movie_name in movie_names:
        q |= Q(name__iexact=movie_name)

    movies_by_given_movie_names = list(Movie.objects.filter(q))
    return get_movies_by_given_movie_names(movies_by_given_movie_names)


def get_all_actor_objects_acted_in_given_movies(movie_objs):
    all_actor_objects_acted_in_given_movies = list(  Cast.objects.values_list('actor').filter(movie__in=movie_objs).distinct() )
    return all_actor_objects_acted_in_given_movies


def get_female_cast_details_from_movies_having_more_than_five_female_cast():
    query = list( Cast.objects.values_list('movie').annotate(female_actors_count = Sum(Case(When (actor__gender = 2,then=1),default=0,output_field=models.IntegerField()))).filter(female_actors_count__gte=5))
    return get_movies_by_given_movie_names(query)