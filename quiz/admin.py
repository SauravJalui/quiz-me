from django.contrib import admin
from . models import Topic, Question, Answer



class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Topic)
admin.site.register(Question,QuestionAdmin)