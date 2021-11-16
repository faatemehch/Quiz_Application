from django.shortcuts import render
from .models import Quiz
from django.views.generic import ListView


class QuizListView( ListView ):
    model = Quiz
    template_name = 'quiz/main-page.html'


def quizView(request, *args, **kwargs):
    quiz_id = kwargs['quiz_id']
    quiz = Quiz.objects.filter( id=quiz_id )
    context = {'quiz': quiz}
    return render( request, 'quiz/quiz-page.html', context )
