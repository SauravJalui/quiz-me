from django.shortcuts import render
from . models import Question

def home(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'quiz/index.html', context)

