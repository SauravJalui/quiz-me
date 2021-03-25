from rest_framework import serializers
from .models import (Category, Question, MCQOptions, 
                     FillInTheBlank, Progress, AnswersGiven)
from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    serializes the user model
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email']


class CategorySerializer(serializers.ModelSerializer):
    """
    serializes the category model (nested with the user serializer)
    """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """
    serializes the question model (nested with category serializer)
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Question
        fields = '__all__'


class MCQOptionsSerializer(serializers.ModelSerializer):
    """
    serializes the MCQOptions model (nested with question serializer)
    """
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = MCQOptions
        fields = '__all__'


class FillInTheBlankSerializer(serializers.ModelSerializer):
    """
    serializes the FillInTheBlank model (nested with question serializer)
    """
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = FillInTheBlank
        fields = '__all__'


class ProgressSerializer(serializers.ModelSerializer):
    """
    serializes the Progress model 
    (nested with user and the category serializer)
    """
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Progress
        fields = '__all__'


class AnswersGivenSerializer(serializers.ModelSerializer):
    """
    serializes the AnswersGiven model 
    (nested with question and the MCQOptions serializer)
    """
    question = QuestionSerializer(read_only=True)
    option_chosen = MCQOptionsSerializer(read_only=True)

    class Meta:
        model = AnswersGiven
        fields = '__all__'
