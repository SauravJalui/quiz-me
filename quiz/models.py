from django.db import models
from accounts.models import CustomUser
from django.urls import reverse
import uuid


class Question(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.question_text)

class User(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return str(self.choice_text)


class Answer(models.Model):
    '''choices for questions'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('answer-detail', kwargs={'pk': self.pk})






