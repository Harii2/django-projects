from django.urls import path
from . import views

urlpatterns = [
    path("", views.index , name="index"),
    path("questions/", views.get_list_of_questions, name="get_list_of_questions"),
    path("questions/create/", views.create_question, name="create_question"),
    path('questions/<int:question_id>/get/', views.get_question, name="get_question"),
    path("questions/<int:question_id>/update/", views.update_question, name="update_question"),
    path("questions/<int:question_id>/delete/", views.delete_question, name="delete question")
]