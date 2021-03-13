from django.urls import path
from . views import ExamListView, ResultPageListView, StartPage

app_name = 'quiz'

urlpatterns = [
    path('', StartPage.as_view(), name='start-page'),
    path('quiz/',
         ExamListView.as_view(), name='question-page'),
    path('results/', ResultPageListView.as_view(), name='result-page'),
]
