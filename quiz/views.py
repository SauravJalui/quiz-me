from django.shortcuts import render, get_object_or_404
from accounts.models import Profile,CustomUser
from django.views.generic import (
    CreateView,
    ListView, 
    DetailView,
)
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .forms import QuestionAnswerForm
from .models import User, Question, Choice, Answer
from .scripts import find_high_score

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


class QuestionFormView(CreateView):
    form_class = QuestionAnswerForm
    model = Answer
    template_name = 'quiz/questions_list.html'

    def get_initial(self):
        initial = super(QuestionFormView, self).get_initial()
        current_question = Question.objects.get(pk=self.kwargs['pk'])
        initial['question'] = Question.objects.get(pk=self.kwargs['pk'])

        # check if the user has already made a choice for this question
        try:
            user_id = self.request.session['user_id']
            selected_id = str(user_id) + "-" + str(current_question.id)
            current_choice_id = self.request.session[selected_id]
            current_choice = Choice.objects.get(pk=current_choice_id)
        except KeyError:
            pass
        else:
            initial['choices'] = current_choice

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_question = Question.objects.get(pk=self.kwargs['pk'])
        context['current_question'] = current_question

        # try and get a previous question
        try:
            prev_id = current_question.id - 1
            prev_question = Question.objects.get(pk=prev_id)
        except (KeyError, Question.DoesNotExist):
            pass
        else:
            context['previous_question'] = prev_question

        # try and get a next question
        try:
            next_id = current_question.id + 1
            next_question = Question.objects.get(pk=next_id)
        except (KeyError, Question.DoesNotExist):
            pass
        else:
            context['next_question'] = next_question

        return context

    def form_invalid(self, form):
        current_question = Question.objects.get(pk=self.kwargs['pk'])
        if 'prev' in self.request.POST:
            prev_question_id = current_question.id - 1
            return HttpResponseRedirect(reverse("quiz:questions_list", args=(prev_question_id,)))

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        current_user = CustomUser.objects.get(pk=self.request.session['user_id'])
        current_question = Question.objects.get(pk=self.kwargs['pk'])

        try:
            selected_choice = current_question.choice_set.get(pk=form.cleaned_data['choices'].id)
        except (KeyError, Choice.DoesNotExist):
            return HttpResponseRedirect(reverse("quiz:questions_list", args=(current_question.pk,)))
        else:
            if selected_choice.correct:
                # check if this choice has already been selected
                try:
                    user_choice_key = str(current_user.id) + "-" + str(current_question.id)
                    previous_choice = current_question.choice_set.get(pk=self.request.session[user_choice_key])
                    if previous_choice == selected_choice:
                        pass
                    else:
                        # save the selected choice using session data
                        user_choice_key = str(current_user.id) + "-" + str(current_question.id)
                        self.request.session[user_choice_key] = selected_choice.id
                        # this hasn't been selected
                        current_user.score += 1
                        current_user.save()
                except KeyError:
                    # save the selected choice using session data
                    user_choice_key = str(current_user.id) + "-" + str(current_question.id)
                    self.request.session[user_choice_key] = selected_choice.id
                    # this hasn't been selected
                    current_user.score += 1
                    current_user.save()
                else:
                    pass
            else:
                # save the selected choice using session data
                user_choice_key = str(current_user.id) + "-" + str(current_question.id)
                self.request.session[user_choice_key] = selected_choice.id

        new_question_id = current_question.id + 1
        try:
            Question.objects.get(pk=new_question_id)
        except (KeyError, Question.DoesNotExist):
            user_id = self.request.session['user_id']
            return HttpResponseRedirect(reverse("quiz:results", args=(user_id,)))

        return HttpResponseRedirect(reverse("quiz:questions_list", args=(new_question_id,)))


class ResultsView(DetailView):
    model = CustomUser
    template_name = 'quiz/results.html'

    def get_context_data(self, **kwargs):
        current_user = CustomUser.objects.get(pk=self.request.session['user_id'])
        users_by_score = CustomUser.objects.all().order_by('-score')
        score_list = []
        for user in users_by_score:
            score_list.append(user.score)
        high_score = find_high_score(score_list)
        return {
            "current_user": current_user,
            "users": users_by_score,
            "high_score": high_score
        }
