from django.http import JsonResponse
from django.shortcuts import render
from .models import Quiz, Question
from django.views.generic import ListView
import random


class QuizListView( ListView ):
    model = Quiz
    template_name = 'quiz/main-page.html'


def quizView(request, *args, **kwargs):
    quiz_id = kwargs['quiz_id']
    quiz = Quiz.objects.filter( id=quiz_id ).first()
    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render( request, 'quiz/quiz-page.html', context )


def checkingView(request, *args, **kwargs):
    quiz: Quiz = Quiz.objects.filter( id=kwargs['quiz_id'] ).first()
    # questions: Question = quiz.question_set.all()
    questions: Question = Question.objects.filter( quiz_id=kwargs['quiz_id'] ).all()

    number_of_correct_questions = 0
    for num, question in enumerate( questions ):
        real_answer = question.get_correct()
        user_answer = request.GET.get( f'{question.question_text}' )
        if real_answer == user_answer:
            number_of_correct_questions += 1
    return render( request, 'quiz/checking.html', {'score': number_of_correct_questions} )
