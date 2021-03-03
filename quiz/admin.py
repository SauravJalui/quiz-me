from django.contrib import admin
from . models import Question, Choice

admin.site.site_header = "Quiz Admin"
admin.site.site_title = "Quiz Admin Area"
admin.site.index_header = "Welcome to the Quiz Admin Area"

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)

