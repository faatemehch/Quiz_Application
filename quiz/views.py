from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect


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
        user = request.user
        form_data = dict( request.POST )
        form_data.pop( 'csrfmiddlewaretoken' )
        number_of_correct_questions = 0
        results = {}
        for question in questions:
            real_answer = question.get_correct()
            user_answer = form_data.get( f'{question}' )  # key => question, value => user-answer
            if user_answer is None:
                results[f'{question}'] = [False, real_answer, user_answer]
            elif real_answer == user_answer[0]:
                number_of_correct_questions += 1
                results[f'{question}'] = [True, real_answer, *user_answer]
            else:
                results[f'{question}'] = [False, real_answer, *user_answer]
        score = (number_of_correct_questions / len( questions )) * 100
        Result.objects.create( quiz_id=kwargs['quiz_id'], owner=user, score=score )
        context = {'score': score, 'results': results}
        if score < quiz.min_score:
            context['passed'] = False
        else:
            context['passed'] = True
        return render( request, 'quiz/checking.html', context )
    return redirect( 'quiz:home-view' )
