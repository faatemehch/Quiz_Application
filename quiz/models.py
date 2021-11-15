from django.contrib.auth.models import User
from django.db import models

choices = (
    ('easy', 'EASY'),
    ('medium', 'MEDIUM'),
    ('hard', 'HARD')
)


class Quiz( models.Model ):
    name = models.CharField( max_length=100 )
    difficulty = models.CharField( choices=choices )
    required_time = models.IntegerField()

    def __str__(self):
        return self.name


class Question( models.Model ):
    question_text = models.CharField( max_length=250 )
    quiz = models.ForeignKey( Quiz, on_delete=models.CASCADE )

    def __str__(self):
        return self.question_text


class Answer( models.Model ):
    question = models.ForeignKey( Question, on_delete=models.CASCADE )
    is_correct = models.BooleanField( default=False )
    answer_text = models.CharField( max_length=200 )

    def __str__(self):
        return f'{self.answer_text} - {self.question.question_text} - {self.question.quiz.name}'


class Result( models.Model ):
    quiz = models.ForeignKey( Quiz, on_delete=models.CASCADE )
    owner = models.ForeignKey( User, on_delete=models.CASCADE )
    score = models.FloatField()

    def __str__(self):
        return f'{self.owner} : {self.quiz} - {self.score}'
