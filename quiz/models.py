from django.db import models
from accounts.models import CustomUser
from datetime import datetime, timedelta
import uuid


class Question(models.Model):
    '''Model for storing MCQ and fill in the blanks questions'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        null=False)
    title = models.CharField(max_length=150)
    
    MCQ = 'MCQ'
    FILLINTHEBLANKS = 'FillInTheBlanks'
    question_choices = [
        (MCQ, 'MCQ'),
        (FILLINTHEBLANKS, 'FillInTheBlanks'),
    ]

    question_type = models.CharField(max_length=15, choices=question_choices)
    user = models.ManyToManyField(CustomUser, through="AnswerGiven")

    def __str__(self):
        return f'{self.title}'


class Mcq(models.Model):
    '''MCQ Questions'''
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100, blank= True)
    option4 = models.CharField(max_length=100, blank= True)
    choices_mcq = [
        (1, (1)),
        (2, (2)),
        (3, (3)),
        (4, (4)),
    ]
    correct_answer_mcq = models.IntegerField(choices=choices_mcq)
    
    class Meta:
        verbose_name_plural = "MCQ's"

    def __str__(self):
        return f'{self.question}'


class FillInTheBlanks(models.Model):
    '''One answer model'''
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE)
    correct_answer_fill_in_the_blanks = models.CharField(
        default="", max_length=100)

    class Meta:
        verbose_name_plural = "Fill In The Blanks"

    def __str__(self):
        return f'{self.question}'


class AnswerGiven(models.Model):
    '''Records the answer given by the user'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE)
    user_answer_mcq = models.IntegerField(default=0)
    user_answer_fill_in_the_blanks = models.CharField(
        default="", max_length=100)
    is_answer_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Answers Given"
    
    def __str__(self):
        return f'{self.question}'

def get_deadline():
    return datetime.now() + timedelta(days=10)

class UserProgress(models.Model):
    '''tracks user progress'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False, 
        unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    current_page = models.IntegerField(default=1)
    user_score = models.IntegerField(default=0)
    user_time = models.DateTimeField(default=datetime.now)
    user_end_time = models.DateTimeField(default=get_deadline)
    has_started = models.BooleanField(default=False)
    has_finished = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User's Progress"

    def __str__(self):
        return f'{self.user.email} Progress'