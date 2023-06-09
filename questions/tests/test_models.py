from unittest import TestCase

from django.contrib.auth.models import User
from faker import factory

from questions.models import Tags, Questions, QuestionVotes, Answers, AnswerVotes


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Questions

class QuestionVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionVotes

class AnswersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answers
    correct = True

class AnswerVotesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnswerVotes

class TagModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        TagFactory(name='Python')

    def test_tag_label(self):
        tag = Tags.objects.get(name='Python')
        field_label = tag._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_tag_str(self):
        tag = Tags.objects.get(name='Python')
        str_tag = str(tag)
        self.assertEqual('Python', str_tag)

class QuestionsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserFactory(username='Test_user')
        QuestionFactory(title='Test_name', author=user)

    def test_question_title_label(self):
        question = Questions.objects.get(title='Test_name')
        title_label = question._meta.get_field('title').verbose_name
        self.assertEqual(title_label, 'Заголовок')

    def test_question_body_label(self):
        question = Questions.objects.get(title='Test_name')
        title_body = question._meta.get_field('body').verbose_name
        self.assertEqual(title_body, 'Текст вопроса')

    def test_question_author_label(self):
        question = Questions.objects.get(title='Test_name')
        author_label = question._meta.get_field('author').verbose_name
        self.assertEqual(author_label, 'author')

    def test_question_create_date_label(self):
        question = Questions.objects.get(title='Test_name')
        date_label = question._meta.get_field('create_date').verbose_name
        self.assertEqual(date_label, 'create_date')

    def test_question_tags_label(self):
        question = Questions.objects.get(title='Test_name')
        tags_label = question._meta.get_field('tags').verbose_name
        self.assertEqual(tags_label, 'tags')

    def test_question_str(self):
        question = Questions.objects.get(title='Test_name')
        self.assertEqual(str(question), 'Test_name Test_user')

class QuestionVotesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserFactory(username='Test_user')
        question = QuestionFactory(author=user)
        QuestionVoteFactory(author=user, question=question)

    def test_question_votes_author_label(self):
        vote = QuestionVotes.objects.get(id=1)
        author_label = vote._meta.get_field('author').verbose_name
        self.assertEqual(author_label, 'author')

    def test_question_votes_create_date(self):
        vote = QuestionVotes.objects.get(id=1)
        create_date_label = vote._meta.get_field('create_date').verbose_name
        self.assertEqual(create_date_label, 'create_date')

    def test_question_votes_question(self):
        vote = QuestionVotes.objects.get(id=1)
        question_label = vote._meta.get_field('question').verbose_name
        self.assertEqual(question_label, 'question')

    def test_question_votes_str(self):
        vote = QuestionVotes.objects.get(id=1)
        self.assertEqual(str(vote), f'Question votes by {vote.author.username}')


class AnswerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserFactory(username='Test_user')
        question = QuestionFactory(author=user)
        QuestionVoteFactory(author=user, question=question)

    def test_answer_body_label(self):
        answer = Answers.objects.get(id=1)
        body_label = answer._meta.get_field('body').verbose_name
        self.assertEqual(body_label, 'Ваш ответ')

    def test_answer_author_label(self):
        answer = Answers.objects.get(id=1)
        author_label = answer._meta.get_field('author').verbose_name
        self.assertEqual(author_label, 'author')

    def test_answer_create_date_label(self):
        answer = Answers.objects.get(id=1)
        create_date_label = answer._meta.get_field('create_date').verbose_name
        self.assertEqual(create_date_label, 'create_date')

    def test_answer_correct_label(self):
        answer = Answers.objects.get(id=1)
        correct_label = answer._meta.get_field('correct').verbose_name
        self.assertEqual(correct_label, 'correct')

    def test_answer_question_label(self):
        answer = Answers.objects.get(id=1)
        question_label = answer._meta.get_field('question').verbose_name
        self.assertEqual(question_label, 'question')

    def test_answer_str(self):
        answer = Answers.objects.get(id=1)
        self.assertEqual(str(answer), f'Answer of Test_user from {answer.create_date}')


class AnswerVotesModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserFactory(username='Test_user')
        question = QuestionFactory(author=user)
        answer = AnswersFactory(author=user, question=question)
        AnswerVotesFactory(author=user, answer=answer)

    def test_answer_votes_author_label(self):
        vote = AnswerVotes.objects.get(id=1)
        author_label = vote._meta.get_field('author').verbose_name
        self.assertEqual(author_label, 'author')

    def test_answer_votes_create_date_label(self):
        vote = AnswerVotes.objects.get(id=1)
        create_date_label = vote._meta.get_field('create_date').verbose_name
        self.assertEqual(create_date_label, 'create_date')

    def test_answer_votes_answer_label(self):
        vote = AnswerVotes.objects.get(id=1)
        answer_label = vote._meta.get_field('answer').verbose_name
        self.assertEqual(answer_label, 'answer')

    def test_answer_votes_str(self):
        vote = AnswerVotes.objects.get(id=1)
        self.assertEqual(str(vote), 'Answer votes by Test_user')

