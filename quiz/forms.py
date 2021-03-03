from django import forms
from django.forms import ModelForm
from .models import User, Answer


class QuestionAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['choices']

    def __init__(self, *args, **kwargs):
        super(QuestionAnswerForm, self).__init__(*args, **kwargs)
        question = self.initial['question']
        self.fields['choices'] = forms.ModelChoiceField(
            queryset=question.choice_set.all(), 
            widget=forms.RadioSelect,
            label="", )