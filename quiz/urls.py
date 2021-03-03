from django.urls import path
from . views import (
    home, 
    Quiz,
    QuestionFormView,
    ResultsView,
)

app_name = 'quiz'

urlpatterns = [
    path('', home, name='home'),
    path('quiz/', Quiz.as_view(), name='quiz'),
    path('quiz/questions/<uuid:pk>/', QuestionFormView.as_view(), name='questions_list'),
    path('quiz/questions/<uuid:pk>/results/', ResultsView.as_view(), name='results'),
]
