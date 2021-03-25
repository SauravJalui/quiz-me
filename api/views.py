from .models import (Category, Question, MCQOptions, 
                     FillInTheBlank, Progress, AnswersGiven)
from .serializers import (CategorySerializer, QuestionSerializer, 
                          MCQOptionsSerializer, FillInTheBlankSerializer, ProgressSerializer, AnswersGivenSerializer)
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework.generics import (ListAPIView, CreateAPIView, 
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class CategoryListView(ListAPIView):
    """
    This apiview displays the categories by title
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = CategorySerializer

    def get_queryset(self, *args, **kwargs):
        final_categories = []
        categories = Category.objects.order_by('title')

        #this returns the first object matched by the queryset (first)\
        #in progress class
        for category in categories:
            progress = Progress.objects.filter(
                user=self.request.user, category=category).first()
            if progress is None:
                final_categories.append(category)
        return final_categories



class QuestionListView(ListAPIView):
    """
    This api displays all the questions filtering it by category
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = QuestionSerializer

    def get_queryset(self, *args, **kwargs):
        return Question.objects.filter(category__id=self.kwargs['category_pk'])



class QuestionDetailsView(APIView):
    """
    This apiview displays the question details (mcq or fill in the blanks)
    """
    permission_classes = [IsAuthenticated,]

    def get(self, request, question_pk):
        data = {}
        #this either gets the question model or 404 depending 
        #on what's available
        question = get_object_or_404(Question, id=question_pk)
        if question.type_of_question == Question.MCQ:
            mcq_options = MCQOptions.objects.filter(question=question)
            serialized_mcqs = []
            for mcq in mcq_options:
                serializer = MCQOptionsSerializer(mcq)
                serialized_mcqs.append(serializer.data)
            data = serialized_mcqs
        if question.type_of_question == Question.FILL_IN_THE_BLANKS:
            fill_in_the_blank = get_object_or_404(
                FillInTheBlank, question=question)
            serializer = FillInTheBlankSerializer(fill_in_the_blank)
            data = serializer.data
        return Response(data=data)



class AttemptQuizView(APIView):
    """
    This apiview checks the question type, calculates result,
    calculates time limit and keeps track of progress.
    """
    permission_classes = [IsAuthenticated,]

    def get(self, request, category_pk):
        #this displays the category of question while returning the
        #first object by the 'first' queryset in progress.
        category = get_object_or_404(Category, id=category_pk)
        progress = Progress.objects.filter(
            category=category, user=request.user).first()

        #if there is no progress data, this creates it adding the time limit
        if progress is None:
            progress = Progress.objects.create(
                category= category,
                start_time= timezone.now(), 
                end_time= timezone.now() + timezone.timedelta(minutes=category.time_limit),
                is_in_progress=True,
                user=request.user)

        #if there is progress present this calculates the remaining time
        if progress:
            difference = progress.end_time-timezone.now()
            if difference < timezone.timedelta(seconds=1):
                data['remaining_seconds'] = 0
            else:
                data['remaining_seconds'] = difference.seconds

        #checking if questions present
        questions_count = Question.objects.filter(category=category).count()
        if questions_count == 0:
            return Response({'data': 'No questions available'})
        data = {'category_id': category_pk}

        #this filters all the questions that the user has attempted
        user_answers = AnswersGiven.objects.filter(
            user=request.user, 
            question__category=category, is_attempted=True).values_list('question')

        #this filters all the question present in the question model
        all_questions = Question.objects.filter(category=category)

        #if the user has attempted all the questions in the questions 
        #model then the 'is_in_progress' flag will be False
        #and the 'is_completed' flag will be True and save the progress.
        if user_answers.count() == all_questions.count():
            #we also check that there are questions present (this is imp)
            #in the question model
            if all_questions.count() > 0:
                progress.is_in_progress = False
                progress.is_completed = True
                progress.save()

        #this filters question excluding the questions that the user
        #has attempted.
        question = Question.objects.filter(
            category=category).exclude(id__in=user_answers).first()

        #if the above filter does not return any result and there is 
        #progress data and if the 'is_completed' flag is True
        #then mark is is completed
        if question is None:
            if progress:
                if progress.is_completed:
                    data['data'] = 'completed'

        else:
            data['question'] = QuestionSerializer(instance=question).data
            if question.type_of_question == Question.MCQ:
                options = MCQOptions.objects.filter(question=question)
                for index, option in enumerate(options):
                    data['option_' +
                         str(index)] = MCQOptionsSerializer(instance=option).data
        return Response(data=data)

    def post(self, request, category_pk):
        request_data = request.data

        #checks the question_if of the data received
        #and checks if it matches with the question_id of a 
        #question present in question model else 404 error
        question_id = request_data['question_id']
        question = get_object_or_404(Question, id=question_id)

        progress = Progress.objects.filter(
            category=question.category, user=request.user).first()

        #checks if the question type that is displayed is mcq 
        if question.type_of_question == Question.MCQ:
            #we also make sure that the user has selected at least 
            #one mcq option before moving ahead
            selected_option_id = request_data.get('selected_option_id', None)
            if(selected_option_id):
                pass
            else:
                return Response(data={'error': ['Select an option']})
            mcq_option = get_object_or_404(MCQOptions, id=selected_option_id)

            #this saves all the data received from the mcq question
            #in user_answers variable to calculate results later.
            user_answers = AnswersGiven.objects.create(
                user=request.user, question=question,
                option_chosen=mcq_option, is_correct=mcq_option.is_correct,
                is_attempted=True)

            #if the option selected is the correct answer then we increase
            #one point and save the progress
            if mcq_option.is_correct:
                progress.marks += 1
                progress.save()
        else:
            #if however the question is fill in the blanks question
            #we check if the user has given an answer, if yes then
            #we save it in variable answer_given for later 
            #result calculation else we ask to enter an answer
            answer_given = request_data.get('answer_given', None)
            if(answer_given):
                pass
            else:
                return Response(data={'error': ['Answer Required']})
            fill_in_the_blank = get_object_or_404(
                FillInTheBlank, question=question)
            is_correct = False
            #when retrieving the answer from the user, the is_correct flag
            #is set to false only after we calculate if the answer user 
            #has given is the correct answer (correct_answer in fill_in_the_blank
            # model) we turn the flag 'is_correct' to true, increase point and 
            #save the progress
            if answer_given.lower() == fill_in_the_blank.correct_answer.lower():
                is_correct = True
                progress.marks += 1
                progress.save()

            #we save all the answers that the user has given for fill in
            #the blanks question in user_answers variable for results
            user_answers = AnswersGiven.objects.create(
                user=request.user, question=question,
                answer_given=answer_given, is_correct=is_correct,
                is_attempted=True)

        return Response({'data': 'Your answer is saved'})


class ResultView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, category_pk):
        data = {}
        try:
            #we get the progress of the authenticated user based on
            #the category id
            progress = Progress.objects.get(
                category__id=category_pk, user=request.user)
            serializer = ProgressSerializer(instance=progress)
            data = serializer.data

            #we filter the questions in each category based on the number
            #of questions
            data['questions_count'] = Question.objects.filter(
                category__id=category_pk).count()

            #we retrieve the answers that the user has given for a 
            #particular category
            user_answers = AnswersGiven.objects.filter(
                user=request.user, question__category__id=category_pk)
            data['user_answers'] = []
            for user_answer in user_answers:
                #we check if the question is mcq and if the answer is correct we 
                #display the answer, if wrong we display the correct answer
                #and same for fill in the blanks
                user_answer_serializer_data = AnswersGivenSerializer(
                    instance=user_answer).data
                if user_answer.question.type_of_question == Question.MCQ:
                    mcq_option = MCQOptions.objects.filter(
                        question=user_answer.question, is_correct=True).first()
                    if mcq_option is not None:
                        user_answer_serializer_data['display_correct_answer'] = mcq_option.option
                else:
                    fill_in_the_blank = FillInTheBlank.objects.get(
                        question=user_answer.question)
                    user_answer_serializer_data['display_correct_answer'] = fill_in_the_blank.correct_answer

                data['user_answers'].append(
                    user_answer_serializer_data)
        except:
            data['error'] = ['Not Found']
        return Response(data)



class ProgressByCategoryListView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProgressSerializer

    def get_queryset(self, *args, **kwargs):
        return Progress.objects.filter(category__id=self.kwargs['category_pk'])



class DashboardView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = {}
        completed_quizzes = Progress.objects.filter(
            user=request.user, is_completed=True)
        data['completed_quiz_list'] = []
        for completed_quiz in completed_quizzes:
            data['completed_quiz_list'].append(
                ProgressSerializer(instance=completed_quiz, 
                                   context={"request": request}).data)
        in_progress_quizzes = Progress.objects.filter(
            user=request.user, is_in_progress=True)
        data['in_progress_quiz_list'] = []
        for in_progress_quiz in in_progress_quizzes:
            data['in_progress_quiz_list'].append(
                ProgressSerializer(instance=in_progress_quiz, context={"request": request}).data)
        return Response(data)



class TimeOverView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, category_pk):
        data = {}

        try:
            progress = Progress.objects.get(
                category__id=category_pk, user=request.user)
            progress.is_completed = True
            progress.is_in_progress = False
            progress.save()
            user_answers = AnswersGiven.objects.filter(
                user=request.user, question__category__id=category_pk).values_list('question')
            questions = Question.objects.filter(
                category__id=category_pk).exclude(id__in=user_answers)

            for question in questions:
                AnswersGiven.objects.create(
                    user=request.user, question=question, is_attempted=True, is_correct=False)
            data['message'] = ["Time's Up!"]
        except Progress.DoesNotExist:
            data['error'] = ['Progress Not Found']
        return Response(data)




class LeaderBoardView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ProgressSerializer

    def get_queryset(self, *args, **kwargs):
        category_pk = self.kwargs['category_pk']
        return Progress.objects.filter(category__id=category_pk, is_completed=True).order_by('-marks')
