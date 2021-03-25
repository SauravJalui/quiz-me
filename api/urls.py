from django.urls import path, include
from .views import (CategoryListView, QuestionListView, QuestionDetailsView,
                    ProgressByCategoryListView,
                    AttemptQuizView, ResultView, DashboardView,
                    TimeOverView, LeaderBoardView)

app_name = 'quiz_api'

urlpatterns = [

    path('category-list/', CategoryListView.as_view(), name='category_list'),
    
    path('question-list/<uuid:category_pk>/',
         QuestionListView.as_view(), name='question_list'),
    path('question-detail/<uuid:question_pk>/',
         QuestionDetailsView.as_view(), name='question_detail'),
    
    path('progress-list/<uuid:category_pk>/',
         ProgressByCategoryListView.as_view(), name='progress_list'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    path('attempt-quiz/<uuid:category_pk>/',
         AttemptQuizView.as_view(), name='attempt_quiz'),
    path('result/<uuid:category_pk>/',
         ResultView.as_view(), name='result'),
    path('time-over/<uuid:category_pk>/',
         TimeOverView.as_view(), name='time_over'),
    path('leaderboard/<uuid:category_pk>/',
         LeaderBoardView.as_view(), name='leaderboard'),

]
