from django.db import models
from accounts.models import CustomUser
import uuid


class Question(models.Model):
    '''This displays the questions'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False)
    question_text = models.CharField(max_length=150)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    choices_mcq = (
        (1, (1)),
        (2, (2)),
        (3, (3)),
        (4, (4)),
    )
    correct_answer_mcq = models.IntegerField(default=0, choices=choices_mcq)
    is_attempted = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

# class Answer(models.Model):
#     '''choices for questions'''
#     id = models.UUIDField(
#         primary_key=True, 
#         default=uuid.uuid4, 
#         editable=False)
#     question = models.ForeignKey(Question,on_delete=models.CASCADE)
#     answer = models.CharField(max_length=150)
#     correct = models.BooleanField(default=False)

#     def __str__(self):
#         return self.answer