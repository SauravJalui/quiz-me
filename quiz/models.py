from django.db import models
from accounts.models import CustomUser
import uuid


class Question(models.Model):
    '''Model for storing MCQ and fill in the blanks questions'''
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        unique=True, 
        null=False)
    title = models.CharField(max_length=150)
    is_mcq = models.BooleanField(default=False)
    is_fill_in_the_blanks = models.BooleanField(default=False)
    user = models.ManyToManyField(CustomUser, through="AnswerGiven")

    def __str__(self):
        return self.title


class MCQ(models.Model):
    '''MCQ Questions'''
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE)
    choice1 = models.CharField(max_length=100)
    choice2 = models.CharField(max_length=100)
    choice3 = models.CharField(max_length=100)
    choice4 = models.CharField(max_length=100)
    choices_mcq = (
        (1, (1)),
        (2, (2)),
        (3, (3)),
        (4, (4)),
    )
    correct_answer_mcq = models.IntegerField(
        default=0, choices=choices_mcq)

    def __str__(self):
        return self.question


class FillInTheBlanks(models.Model):
    '''One answer model'''
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE)
    correct_answer_fill_in_the_blanks = models.CharField(
        default="", max_length=100)

    def __str__(self):
        return self.question


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
    
    def __str__(self):
        return self.question

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
    has_started = models.BooleanField(default=False)
    has_finished = models.BooleanField(default=False)


    def __str__(self):
        return self.user.email + str("'s Progress")