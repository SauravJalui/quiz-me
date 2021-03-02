from django.shortcuts import render, get_object_or_404
from . models import Question
from accounts.models import Profile
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if  request.user.is_authenticated:
        return render(request, 'quiz/index.html', {'profile': get_object_or_404(Profile, user=request.user)})
    else:
        return render(request, 'quiz/index.html')

class Quiz(ListView):
    '''Get questions and display them'''
    model = Question
    template_name = 'quiz/quiz.html'


def Questions_list(request, pk):
    '''Show specific question and choices'''
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'quiz/questions_list.html', { 'question': question })