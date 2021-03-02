from django.shortcuts import render, get_object_or_404
from . models import Question
from accounts.models import Profile


from django.views.generic import ListView

def home(request):
    return render(request, 'quiz/index.html', {'profile': get_object_or_404(Profile, user=request.user)})

class Quiz(ListView):
    '''Get questions and display them'''
    model = Question
    template_name = 'quiz/quiz.html'