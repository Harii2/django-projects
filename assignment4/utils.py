from django.db.models import Q, Avg, Sum, Count, Case, When
from assignment2.models import Actor, Movie, Cast, Director, Rating
from  django.db import models


def get_average_box_office_collections():
    avg_collections = Movie.objects.aggregate(avg_collections=Avg('box_office_collection_in_crores'))
    return round(avg_collections["avg_collections"], 3)


def get_movies_with_distinct_actors_count():
    movies_with_distinct_actors_count = list( Cast.objects.values('movie').annotate(actors_count = Count('actor',distinct = True)) )
    return movies_with_distinct_actors_count


def get_male_and_female_actors_count_for_each_movie():
    male_and_female_actors_count_for_each_movie = list(Cast.objects.
                                                       values('movie').
                                                       annotate( male_actors_count=Sum(
                                                                            Case(When(actor__gender=1,then=1)
                                                                                  ,default=0,
                                                                                  output_field=models.IntegerField())),
                                                                female_actors_count =Sum(
                                                                            Case(When(actor__gender=2,then=2),
                                                                                 default=0,
                                                                                 output_field=models.IntegerField()))
                                                                )
                                                    )
    return male_and_female_actors_count_for_each_movie


def get_roles_count_for_each_movie():
    roles_count_for_each_movie = list(Cast.objects.values('movie').annotate(roles_count = Count('role',distinct = True)))
    return  roles_count_for_each_movie


def get_role_frequency():
    query =list(Cast.objects.values('role').annotate(actors_count = Count('actor',distinct = True)))
    roles_frequency = []
    for role in query:
        role_obj = { role['role'] : role['actors_count']}
        roles_frequency.append((role_obj))
    return roles_frequency


def get_role_frequency_in_order():
    # Doubt
    role_frequency_in_order = list( Cast.objects.values_list('role','actor__actor_id').annotate(count = Count('movie')) )
    return role_frequency_in_order


def get_no_of_movies_and_distinct_roles_for_each_actor():
    no_of_movies_and_distinct_roles_for_each_actor = list( Cast.objects.values_list('actor').annotate(movies_count = Count('movie'),roles_count = Count('role',distinct = True)) )
    return no_of_movies_and_distinct_roles_for_each_actor

def get_movies_with_atleast_forty_actors():
    movies_with_atleast_forty_actors = list( Cast.objects.values_list('movie').annotate(actors_count = Count('actor')).filter(actors_count__gte = 40) )
    return movies_with_atleast_forty_actors


def get_average_no_of_actors_for_all_movies():
    query = list( Movie.objects.aggregate(Avg('cast__actor')) )
    return query