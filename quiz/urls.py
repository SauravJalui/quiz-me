from django.urls import path
from . views import home, Quiz, Questions_list

app_name = 'quiz'

urlpatterns = [
    path('', home, name='home'),
    path('quiz/', Quiz.as_view(), name='quiz'),
    path('quiz/questions/<uuid:pk>/', Questions_list, name='questions_list'),
]
