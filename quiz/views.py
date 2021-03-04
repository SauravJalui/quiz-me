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


class QuestionsList(DetailView):
    '''Show specific question and choices'''
    template_name = 'quiz/quiz.html'
    context_object_name = 'question'
    
    def get_object(self):
        return Question.objects.filter(is_attempted=False).first()