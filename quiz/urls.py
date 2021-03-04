from django.urls import path
from . views import home, QuestionsList

app_name = 'quiz'

urlpatterns = [
    path('', home, name='home'),
    path('quiz/', QuestionsList.as_view(), name='quiz'),
    # path('quiz/questions/<uuid:pk>/', QuestionsList.as_view(), name='questions_list'),
]
