from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.checks import Tags
from django.db.models.fields import json
from django.urls import reverse
from faker import factory
from pywin.dialogs import status

from api.views import GetQuestion, GetSearchQuestion, GetAnswers
from questions.models import Questions, Answers


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags
    name = factory.Faker('name')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Questions

class AnswersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answers

    correct = True


class APITestCase:
    pass


class APIRequestFactory:
    pass


def force_authenticate(request, user):
    pass


class IndexApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetQuestion.as_view({'get': 'list'})
        self.url = reverse('api:index')
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        for i in range(25):
            QuestionFactory(title='Test_name', author=user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user('test', email='testuser@test.com', password='test')

    def test_index_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_index_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.asserGreater(len(response_dict['next']), 1)
        self.assertEqual(response_dict['count'], 25)

class GetQuestionApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetQuestion.as_view({'get': 'retrieve'})
        self.url = reverse('api:getquestion', args=(1,))
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        question = QuestionFactory(title='Test_name', author=user)
        for i in range(3):
            tag = TagFactory()
            question.tags.add(tag)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user('test', email='testuser@test.com', password='test')

    def test_get_question_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_question_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.asserEqual(response_dict['title'], 'Test_name')
        self.assertEqual(len(response_dict['tag']), 3)

class GetSearchRequestApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetSearchQuestion.as_view({'get': 'list'})
        self.url = reverse('api:searchresult') + '?search=Test'
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        for i in range(25):
            QuestionFactory(title='Test_name', author=user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user('test', email='testuser@test.com', password='test')

    def test_search_result_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_result_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.asserGreater(len(response_dict['next']), 1)
        self.assertEqual(response_dict['count'], 25)

class GetAnswersApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetAnswers.as_view({'get': 'list'})
        self.url = reverse('api:getanswers', args=(1,))
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        question = QuestionFactory(title='Test_name', author=user)
        for i in range(25):
            QuestionFactory(question=question, author=user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user('test', email='testuser@test.com', password='test')

    def test_get_answer_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_answer_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.asserGreater(len(response_dict['next']), 1)
        self.assertEqual(response_dict['count'], 25)




