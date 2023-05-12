from django.contrib.admin import ModelAdmin
from django.core.checks import Tags

from api import admin
from questions.models import Questions, Answers, QuestionVotes, AnswerVotes


@admin.register(Tags)
class TagsAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Questions)
class QuestionsAdmin(ModelAdmin):
    list_display = ('id', '__str__')

@admin.register(Answers)
class AnswersAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'correct')

@admin.register(QuestionVotes)
class AnswersAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'create_date')

@admin.register(AnswerVotes)
class AnswersAdmin(ModelAdmin):
    list_display = ('id', '__str__', 'create_date')