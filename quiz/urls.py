from django.urls import path
from .views import (
    QuizListView,
    quizView,
    checkingView
)

app_name = 'quiz'
urlpatterns = [
    path( '', QuizListView.as_view(), name='home-view' ),
    path( '<int:quiz_id>', quizView, name='quiz' ),
    path( 'check/<int:quiz_id>', checkingView, name='quiz-check' ),
]
