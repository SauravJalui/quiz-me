from django.urls import path
from . views import home, Quiz

app_name = 'quiz'

urlpatterns = [
    path('', home, name='home'),
    path('quiz/', Quiz.as_view(), name='quiz'),
]
