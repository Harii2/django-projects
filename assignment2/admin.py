from django.contrib import admin

# Register your models here.
from .models import Movie, Actor, Director, Rating, Gender, Cast

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Rating)
admin.site.register(Cast)
admin.site.register(Gender)

