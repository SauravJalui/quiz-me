from django.contrib import admin
from .models import (Category, Question, MCQOptions, 
                     FillInTheBlank, Progress, AnswersGiven)

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(MCQOptions)
admin.site.register(FillInTheBlank)
admin.site.register(Progress)
admin.site.register(AnswersGiven)
