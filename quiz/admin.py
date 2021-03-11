from django.contrib import admin
from . models import (
    Question, 
    Mcq, 
    FillInTheBlanks, 
    AnswerGiven, 
    UserProgress
)

admin.site.site_header = "QuizMe Admin"
admin.site.site_title = "QuizMe Admin Area"



admin.site.register(Question)
admin.site.register(Mcq)
admin.site.register(FillInTheBlanks)
admin.site.register(AnswerGiven)
admin.site.register(UserProgress)
