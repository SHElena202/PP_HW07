from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField

from questions.models import Questions, Answers


class QuestionCreateForm(ModelForm):

    class Meta:
        model = Questions
        fields = ['title', 'body']

    tags = CharField(max_length=50, label = 'Теги')

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(',')
        if len(tags)> 3:
            raise ValidationError('Необходимо указать не более трех тегов')
        return data

class AnswerCreateForm(ModelForm):
    class Meta:
        model = Answers
        fields = ['body']

