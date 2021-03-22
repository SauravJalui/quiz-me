from accounts.models import CustomUser
from django.views.generic import ListView, TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils import decorators
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import (
    HttpResponseRedirect, reverse, get_object_or_404
)
from datetime import datetime, timedelta
from .models import (
    UserProgress, 
    Mcq, 
    Question, 
    AnswerGiven, 
    FillInTheBlanks
)
from .decorators import (
    does_user_has_permission, 
    does_user_has_permission_for_result_page
)
decorators_for_exam_view = [login_required, does_user_has_permission()]
decorators_for_result_view = [login_required,
                              does_user_has_permission_for_result_page()]


@method_decorator(decorators_for_exam_view, name='dispatch')
class ExamListView(ListView):
    """
    view to represent all the questions in the database
    """
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 1

    
    def get_queryset(self, **kwargs):
        questions = Question.objects.all()
        actual_page = self.request.GET.get('page', 1)
        user_progress = get_object_or_404(UserProgress,
                                          user=self.request.user)

        if int(actual_page) == 1 and user_progress.has_started is False:
            total_minutes = Question.objects.all().count()
            user_progress.user_time = datetime.now()

            user_progress.user_end_time = user_progress.user_time + \
                timedelta(minutes=total_minutes)
            user_progress.has_started = True
            user_progress.has_finished = False
            user_progress.user_score = 0
            AnswerGiven.objects.filter(user=self.request.user).delete()

        user_progress.current_page = actual_page
        user_progress.save()

        return questions

    def get_context_data(self, **kwargs):
        context = super(ExamListView, self).get_context_data(**kwargs)
        user_progress = get_object_or_404(UserProgress,
                                          user=self.request.user)
        context['mcqs'] = Mcq.objects.all()
        context['end_time'] = user_progress.user_end_time
        context['start_time'] = user_progress.user_time
        return context


class ExamCalculationView(View):
    def post(self, request, *args, **kwargs):
        """
        Post the user answer
        """
        post_data = {
            "user_answer": request.POST.get('user_answer'),
            "question_id": request.POST.get('question_id')
        }
        question_data = self.request.POST.get('user_answer', None)
        question_id = self.request.POST.get('question_id', None)

        user_progress = get_object_or_404(UserProgress,
                                          user=self.request.user)
        question = get_object_or_404(Question, id=question_id)
        if question_data is not None:
            mcq = Mcq.objects.all()
            fill_in_the_blanks = FillInTheBlanks.objects.all()
            if question.question_type == 'MCQ':
                for mcq in mcq:
                    if question.id == mcq.question.id:
                        answer_given = AnswerGiven(
                            user=self.request.user, question=question,
                            user_answer_mcq=question_data)
                        if int(answer_given.user_answer_mcq) == mcq.correct_answer_mcq:
                            answer_given.is_answer_correct = True
                            user_progress.user_score += 1
                        answer_given.save()

            elif question.question_type == "FillInTheBlanks":
                for fill_in_the_blanks in fill_in_the_blanks:
                    if question.id == fill_in_the_blanks.question.id:

                        answer_given = AnswerGiven(
                            user=self.request.user, question=question,
                            user_answer_fill_in_the_blanks=question_data)
                        if fill_in_the_blanks.correct_answer_fill_in_the_blanks.upper() == question_data.upper():
                            answer_given.is_answer_correct = True
                            user_progress.user_score += 1
                        else:
                            answer_given.is_answer_correct = False
                        answer_given.save()

        total_count = Question.objects.all().count()
        if total_count == user_progress.current_page:
            user_progress.has_finished = True
            user_progress.save()
            return HttpResponseRedirect(reverse('quiz:result_page'))

        else:
            user_progress.has_finished = False
            user_progress.save()
            question_page = reverse('quiz:question_page')
            return_next_page = f'{question_page}?page={user_progress.current_page+1}'
            return HttpResponseRedirect(return_next_page)


@method_decorator(decorators_for_result_view, name='dispatch')
class ResultPageListView(ListView):
    """
    View to represent user results
    """
    template_name = 'result.html'
    context_object_name = 'answer_given'

    def get_queryset(self, **kwargs):

        answer_given = AnswerGiven.objects.filter(user=self.request.user)
        actual_page = 1
        user_progress = get_object_or_404(UserProgress,
                                          user=self.request.user)
        user_progress.current_page = actual_page
        user_progress.has_finished = True
        user_progress.save()
        return answer_given

    def get_context_data(self, **kwargs):
        context = super(ResultPageListView, self).get_context_data(**kwargs)
        user_progress = get_object_or_404(UserProgress,
                                          user=self.request.user)
        user_score = user_progress.user_score
        context['question'] = Question.objects.all()
        context['mcq'] = Mcq.objects.all()
        context['fill_in_the_blanks'] = FillInTheBlanks.objects.all()
        context['user_score'] = user_score
        context['total_questions'] = Question.objects.all().count()

        return context


class StartPage(TemplateView):
    template_name = 'start_page.html'
    model = CustomUser
