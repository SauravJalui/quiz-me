from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import CustomUser
import uuid


class Category(models.Model):
    """
    category of questions for quiz with time limit
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    time_limit = models.IntegerField(default=0, help_text='time in minutes')
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    """
    type of question, mcq or fill in the blanks
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    question_title = models.CharField(max_length=100)
    MCQ = 'MCQ'
    FILL_IN_THE_BLANKS = 'FILL_IN_THE_BLANKS'
    TYPE_CHOICES = [
        (MCQ, 'MCQ'),
        (FILL_IN_THE_BLANKS, 'Fill in the blanks'),
    ]
    type_of_question = models.CharField(
        max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.category} | {self.question_title}'

    class Meta:
        verbose_name_plural = 'Questions'



class MCQOptions(models.Model):
    """
    mcq options, includes question, its options and correct answer
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question} | {self.option}'
    
    class Meta:
        verbose_name_plural = 'MCQs'


class FillInTheBlank(models.Model):
    """
    fill in the blanks question, has question and its correct answer
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.question} | {self.correct_answer}'
    
    class Meta:
        verbose_name_plural = 'Fill In The Blanks'


class Progress(models.Model):
    """
    user progress stored here
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    marks = models.IntegerField(default=0)
    is_in_progress = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} | {self.category}'
    
    class Meta:
        verbose_name_plural = 'Progress'


class AnswersGiven(models.Model):
    """
    saves all the answers given by user here
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option_chosen = models.ForeignKey(
        MCQOptions, on_delete=models.PROTECT, blank=True, null=True)
    answer_given = models.CharField(
        max_length=100, blank=True, null=True)
    is_correct = models.BooleanField()
    is_attempted = models.BooleanField()

    def __str__(self):
        return f'{self.student} | {self.question}'

    class Meta:
        verbose_name_plural = 'Answers Given'