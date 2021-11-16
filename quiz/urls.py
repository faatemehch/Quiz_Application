from django.urls import path
from .views import (
    QuizListView,
    quizView
)

app_name = 'quiz'
urlpatterns = [
    path( '', QuizListView.as_view(), name='home-view' ),
    path( '<quiz_id>', quizView, name='quiz' )
]
