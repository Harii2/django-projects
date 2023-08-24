from django.db.models import Q, Avg, Sum, Count
from assignment2.models import Actor, Movie, Cast, Director,Rating

from assignment2.utils import get_average_rating_of_movie


def return_movie_object(movie_obj):
    cast = list(
        Cast.objects.filter(movie=movie_obj).values_list('actor__name', 'actor__actor_id', 'role', 'is_debut_movie')
    )
    cast_list = []
    for actor in cast:
        actor_obj = {
            "actor": {
                "name": actor[0],
                "actor_id": actor[1]
            },
            "role": actor[2],
            "is_debut_movie": actor[3]
        }
        cast_list.append(actor_obj)

    obj = {"movie_id": movie_obj.movie_id, "name": movie_obj.name, "cast": cast_list,
           "box_office_collection_in_crores": movie_obj.box_office_collection_in_crores,
           "release_date": movie_obj.release_date, "director_name": movie_obj.director.name,
           "average_rating": get_average_rating_of_movie(movie_obj),
           "total_number_of_ratings": get_average_rating_of_movie(movie_obj) * 5}

    return obj


def get_movies_by_given_movie_names(movie_names):
    movies_list = []
    for movie_obj in movie_names:
        movies_list.append(return_movie_object(movie_obj))

    return movies_list


def get_movies_released_in_summer_in_given_years():
    movies_query = list(Movie.objects.filter(release_date__year__range=[2005, 2010], release_date__month__in=[5, 6, 7]))
    movies_released_in_summer = []
    for movie_obj in movies_query:
        movies_released_in_summer.append(movie_obj)

    return movies_released_in_summer


def get_movie_names_with_actor_name_ending_with_smith():
    movies_with_actor_name_ending_with_smith = list(
        Cast.objects.filter(actor__name__iendswith='smith').values_list('movie__name').distinct())
    return movies_with_actor_name_ending_with_smith


def get_movie_names_with_ratings_in_given_range(ll, ul):
    movies_in_given_range_ratings = list(
        Movie.objects.filter(rating__rating_five_count__gte=ll, rating__rating_five_count__lt=ul))
    return movies_in_given_range_ratings


def get_movie_names_with_ratings_above_given_minimum():
    release_date = Q(release_date__year__gt=2000)
    q5 = Q(rating__rating_five_count__gte=500)
    q4 = Q(rating__rating_four_count__gte=1000)
    q3 = Q(rating__rating_three_count__gte=2000)
    q2 = Q(rating__rating_two_count__gte=4000)
    q1 = Q(rating__rating_one_count__gte=1000)
    query = release_date & (q1 | q2 | q3 | q4 | q5)
    movies_list = list(Movie.objects.filter(query))

    return movies_list


def get_movie_directors_in_given_year(year):
    directors_list = list(Movie.objects.values_list('director__name').annotate(no_of_movies=Count('movie_id')).filter(
        release_date__year=year, no_of_movies__gt=1))
    return directors_list


def get_actor_names_debuted_in_21st_century():
    actor_name_debut_21st_century = list(Cast.objects.values_list('actor__name').filter(is_debut_movie=True,
                                                                                        movie__release_date__year__gt=2000).distinct())
    return actor_name_debut_21st_century


def get_director_names_containing_big_as_well_as_movie_in_may():
    # if use chaining
    director_names_containing_big_as_well_as_movie_in_may = list(
        Movie.objects.values_list('director__name').filter(Q(name__icontains='big') | Q(release_date__month=5)))
    return director_names_containing_big_as_well_as_movie_in_may


def get_director_names_containing_big_and_movie_in_may():
    director_names_containing_big_and_movie_in_may = list( Movie.objects.values_list('director__name').filter(name__icontains = 'big', release_date__month = 5) )
    return director_names_containing_big_and_movie_in_may


def reset_ratings_for_movies_in_this_year():
    movie_ratings_in_2000_year = Rating.objects.filter(movie__release_date__year = 2000)
    movie_ratings_in_2000_year.update(rating_one_count = 0,rating_two_count =0,rating_three_count=0,rating_four_count=0,rating_five_count=0)
    return "Update Succesfully"