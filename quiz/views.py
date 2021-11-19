from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Quiz, Question, Result
from django.views.generic import ListView


class QuizListView( ListView ):
    model = Quiz
    template_name = 'quiz/main-page.html'


@login_required
def quizView(request, *args, **kwargs):
    quiz_id = kwargs['quiz_id']
    quiz = Quiz.objects.filter( id=quiz_id ).first()
    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render( request, 'quiz/quiz-page.html', context )


@login_required
def checkingView(request, *args, **kwargs):
    if request.POST:
        quiz: Quiz = Quiz.objects.get( id=kwargs['quiz_id'] )
        questions = quiz.question_set.all()
        # questions: Question = Question.objects.filter( quiz_id=kwargs['quiz_id'] ).all()
        user = request.user
        form_data = dict( request.POST )
        form_data.pop( 'csrfmiddlewaretoken' )
        number_of_correct_questions = 0
        results = {}
        for key, value in form_data.items():  # key => question, value => user-answer
            user_answer = value[0]
            question: Question = Question.objects.get( question_text=f'{key}' )
            real_answer = question.get_correct()
            if real_answer == user_answer:
                number_of_correct_questions += 1
                results[f'{question}'] = [True, real_answer]
            else:
                results[f'{question}'] = [False, real_answer]

        score = (number_of_correct_questions / len( questions )) * 100
        Result.objects.create( quiz_id=kwargs['quiz_id'], owner=user, score=score )
        context = {'score': score, 'results': results}
        if score < quiz.min_score:
            context['passed'] = False
        else:
            context['passed'] = True
        return render( request, 'quiz/checking.html', context )
    return redirect( 'quiz:home-view' )
