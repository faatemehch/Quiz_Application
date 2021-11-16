from django.contrib import admin
from .models import Quiz, Question, Answer, Result


class AnswerTabular( admin.TabularInline ):
    model = Answer


class QuestionAdmin( admin.ModelAdmin ):
    inlines = [AnswerTabular]
    list_display = ['__str__', 'quiz']


class AnswerAdmin( admin.ModelAdmin ):
    list_display = ['__str__', 'is_correct', 'question']


admin.site.register( Quiz )
admin.site.register( Question, QuestionAdmin )
admin.site.register( Answer, AnswerAdmin )
admin.site.register( Result )
