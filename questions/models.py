from django.contrib.auth.models import User
from django.db.models import Model, TextField, ForeignKey, DateTimeField, ManyToManyField, DO_NOTHING, Count, CASCADE, \
    BooleanField
from django.forms import CharField


class Tags(Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = CharField(max_length=50)

    def __str__(self):
        return self.name


class Questions(Model):
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    title = CharField(max_length=50, verbose_name='Заголовок')
    body = TextField(verbose_name='Текст вопроса')
    author = ForeignKey(User, on_delete=DO_NOTHING)
    create_date = DateTimeField(auto_now_add=True)
    tags = ManyToManyField(Tags)

    def __str__(self):
        return f'{self.title} {self.author.username}'

    @staticmethod
    def get_trends():
        return Questions.objects.annotate(count=Count('questionvotes')).order_by('-count')[:20]


class QuestionVotes(Model):
    class Meta:
        verbose_name = 'Question vote'
        verbose_name_plural = 'Question votes'

    author = ForeignKey(User, on_delete=DO_NOTHING)
    create_date = DateTimeField(auto_now_add=True)
    question = ForeignKey(Questions, on_delete=CASCADE)

    def __str__(self):
        return f'Question votes by {self.author.username}'


class Answers(Model):
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    body = TextField(max_length=1000, verbose_name='Ваш ответ')
    author = ForeignKey(User, on_delete=DO_NOTHING)
    create_date = DateTimeField(auto_now_add=True)
    correct = BooleanField(blank=True)
    question = ForeignKey(Questions, on_delete=CASCADE)

    def __str__(self):
        return f'Answer of {self.author.username} from {self.create_date}'


class AnswerVotes(Model):
    class Meta:
        verbose_name = 'Answer vote'
        verbose_name_plural = 'Answer votes'

    author = ForeignKey(User, on_delete=DO_NOTHING)
    create_date = DateTimeField(auto_now_add=True)
    answer = ForeignKey(Answers, on_delete=CASCADE)

    def __str__(self):
        return f'Answer votes by {self.author.username}'
