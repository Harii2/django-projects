from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .models import Question
import json


def index(req):
    return HttpResponse("Hey Hello From Assignment1")


def get_list_of_questions(req):
    all_questions = Question.objects.all()
    sort_by = req.GET.get('sort_by')
    data = {
        "questions" : all_questions
    }
    print(sort_by)
    if sort_by and sort_by == 'asc':
        data = {
            "questions" : Question.objects.all().order_by("text")
        }
    elif sort_by and sort_by == 'desc':
        data = {
            "questions" : Question.objects.all().order_by("-text")
        }
    return render(req, 'get_list_of_questions.html', data)


def create_question(req):
    if req.method == "GET":
        return render(req, 'create_question_form.html')
    question = req.POST.get("question")
    answer = req.POST.get("answer")
    if question == "" or answer == "":
        return render(req, 'create_question_failure.html')

    obj = Question.objects.create(text = question, answer = answer)

    try :
        obj.save()
        return render(req,'create_question_success.html')
    except Exception as e :
        return render(req, 'create_question_failure.html')


def get_question(req, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        data = {
            "question": question
        }
        return render(req, 'each_question_form.html', data)
    except ObjectDoesNotExist:
        return render(req, 'question_not_found.html')


def update_question(req, question_id):
    text = req.POST.get('question')
    answer = req.POST.get('answer')
    if text == '' or answer == '':
        return render(req, 'update_question_failure.html')
    if req.method == "POST":
        question = Question.objects.get(id = question_id)
        question.text = text
        question.answer = answer
        question.save()
        return render(req, 'update_question_success.html')


def delete_question(req, question_id):
    try:
        question = Question.objects.get(id=question_id)
        question.delete()
        return render(req, 'delete_question_success.html')
    except ObjectDoesNotExist:
        return render(req, 'delete_question_failure.html')