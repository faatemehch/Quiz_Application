from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Quiz, Question, Result
from django.views.generic import ListView


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
    if request.POST:
        questions: Question = Question.objects.filter( quiz_id=kwargs['quiz_id'] ).all()
        user = User.objects.filter( id=request.user.id ).first()

        form_data = dict( request.POST )
        form_data.pop( 'csrfmiddlewaretoken' )

        number_of_correct_questions = 0
        for num, question in enumerate( questions ):
            real_answer = question.get_correct()
            user_answer = request.POST.get( f'{question.question_text}' )
            if real_answer == user_answer:
                number_of_correct_questions += 1
        score = (number_of_correct_questions / len( questions )) * 100
        Result.objects.create( quiz_id=kwargs['quiz_id'], owner=user, score=score )
        return render( request, 'quiz/checking.html', {'score': score} )
    return redirect( 'quiz:home-view' )
