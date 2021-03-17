from .models import UserProgress
from django.shortcuts import (
    get_object_or_404, HttpResponseRedirect, reverse
)
from django.contrib import messages
from datetime import datetime


def does_user_has_permission():
    '''checks if user can go back to last question, \
        access the quiz after timer has run out, \
            attempt the quiz more than once'''
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            user_progress = get_object_or_404(UserProgress,
                                              user=request.user)
            actual_page = request.GET.get('page', 1)

            if user_progress.user_end_time < \
                    datetime.now(user_progress.user_end_time.tzinfo):
                message = "Sorry, you can't access the questions, You ran out of time."
                messages.warning(request, message)
                return HttpResponseRedirect(reverse('quiz:result_page'))

            if user_progress.has_finished is True:
                message = "Since you have already attempted all the questions of the quiz once, you can't access them again"
                messages.warning(request, message)
                return HttpResponseRedirect(reverse('quiz:result_page'))

            if (int(actual_page) >= user_progress.current_page):
                return view_func(request, *args, **kwargs)

            if (int(actual_page) < user_progress.current_page):
                message = "You can't go back"
                messages.warning(request, message)
                saved_page = reverse('quiz:question_page')
                return_next_page = f'{saved_page}?page={user_progress.current_page}'
                return HttpResponseRedirect(return_next_page)
        return wrap
    return decorator


def does_user_has_permission_for_result_page():
    '''checks if the user can go directly to the \
        results page before finishing the quiz'''
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            user_progress = get_object_or_404(UserProgress,
                                              user=request.user)
            actual_page = request.GET.get('page', 1)
            if user_progress.user_end_time < \
                    datetime.now(user_progress.user_end_time.tzinfo):
                user_progress.current_page = 1
                user_progress.has_finished = True

            if user_progress.has_finished is False:
                message = "No access to the result page! Please finish quiz first"
                messages.warning(request, message)
                saved_page = reverse('quiz:question_page')
                return_next_page = f'{saved_page}?page={user_progress.current_page}'
                return HttpResponseRedirect(return_next_page)
            else:
                return view_func(request, *args, **kwargs)
        return wrap
    return decorator
