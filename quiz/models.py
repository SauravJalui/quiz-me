from django.db import models
import uuid


class Topic(models.Model):
    '''This defines the topic of each question '''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Question(models.Model):
    '''This displays the questions'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    question = models.CharField(max_length=150)

    def __str__(self):
        return self.question

class Answer(models.Model):
    '''choices for questions'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=150)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer