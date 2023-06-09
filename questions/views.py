from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, RedirectView

from questions.forms import QuestionCreateForm, AnswerCreateForm
from questions.models import Questions, Tags, Answers, QuestionVotes, AnswerVotes
from registration.models import UserProfile


class IndexView(ListView):
    model = Questions
    template_name = 'questions/index.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            context['photo'] = self.request.user.userprofile.photo
        if self.request.session.get('order') == 'date':
            context['order_date'] = 'active'
        else:
            context['order_popular'] = 'active'
        tag = self.request.GET.get('tag')
        if tag:
            context['tag_value'] = f'tag:{tag}'
        context['trends'] = Questions.get_trends()
        return context

    def get_queryset(self):
        if self.request.GET.get('order'):
            self.request.session['order'] = self.request.GET['order']
        elif self.request.session.get('order') is None:
            self.request.session['order'] = 'popular'
        if self.request.session.get('order') == 'date':
            order = '-create_date'
        elif self.request.session.get('order') == 'popular':
            order = '-count_votes'
        return Questions.objects.annotate(
            count_votes=Count('questionvotes', distinct=True),
            count_answers=Count('answers', distinct=True)
        ).order_by(order)

class CreateQuestionView(CreateView):
    template_name = 'questions/new_question.html'
    form_class = QuestionCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['photo'] = self.request.user.userprofile.photo
        context['trends'] = Questions.get_trends()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        for tag in form.cleaned_data['tags'].split(','):
            new_tag, _ = Tags.objects.get_or_create(name=tag)
            self.object.tags.add(new_tag)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('questions:questionview', args=[self.object.id])


class QuestionView(ListView):
    model = Answers
    template_name = 'questions/question_detail.html'
    paginate_by = 30

    def get_queryset(self):
        self.question = get_object_or_404(Questions, pk=self.kwargs.get('pk'))
        queryset = Answers.objects.filter(question=self.question).annotate(count=Count('answervotes')).order_by('-count', '-create_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number_question_votes = QuestionVotes.objects.filter(question=self.question).count()
        context['number_question_votes'] = number_question_votes
        context['question'] = self.question
        if self.request.user.is_authenticated:
            context['photo'] = self.request.user.userprofile.photo
            if self.request.user != self.question.author:
                context['disabled_correct_answer'] = 'disabled'
        else:
            context['disabled_correct_answer'] = 'disabled'
            context['disabled'] = 'disabled'
        form = AnswerCreateForm()
        context['form'] = form
        tag = self.request.GET.get('tag')
        if tag:
            context['tag_value'] = f'tag:{tag}'
        context['trends'] = Questions.get_trends()
        return context

    def post(self, request, pk):
        form = AnswerCreateForm(request, POST)
        if form.is_valid():
            new_answer = Answers(
                body=form.cleaned_data['body'],
                author=request.user,
                question=Questions.objects.get(id=pk),
                correct=False,
            )
            new_answer.save()
            question_link = request._current_scheme_host + request.path
            send_mail(
                subject='Получен ответ на ваш вопрос',
                msg=f'Ссылка на ваш вопрос {question_link}',
                from_email='info@homework.ru',
                recipient_list=[request.user.email],
                fail_silently=True,
            )
            return redirect(f'/question/{pk}')

class QuestionVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        new_vote, created = QuestionVotes.objects.get_or_create(author=self.request.user, question_id=pk)
        if created:
            new_vote.save()
        current_page = self.request.GET.get('page')
        self.url = reverse('questions:questionview', args=[pk]) +f'?page={current_page}'
        return super().get_redirect_url(*args, **kwargs)

class QuestionUnVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        with transaction.atomic():
            vote = QuestionVotes.objects.filter(author=self.request.user, question_id=pk).first()
            if vote:
                vote.delete()
        current_page = self.request.GET.get('page')
        self.url = reverse('questions:questionview', args=[pk]) +f'?page={current_page}'
        return super().get_redirect_url(*args, **kwargs)


class AnswerVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        id_answer = kwargs['id_answer']
        new_vote_answer, created = AnswerVotes.objects.get_or_create(author=self.request.user, answer_id=id_answer)
        if created:
            new_vote_answer.save()
        current_page = self.request.GET.get('page')
        self.url = reverse('questions:questionview', args=[pk]) + f'?page={current_page}'
        return super().get_redirect_url(*args, **kwargs)


class AnswerUnVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        id_answer = kwargs['id_answer']
        with transaction.atomic():
            vote_answer = AnswerVotes.objects.filter(author=self.request.user, answer_id=id_answer).first()
            if vote_answer:
                vote_answer.delete()
        current_page = self.request.GET.get('page')
        self.url = reverse('questions:questionview', args=[pk]) +f'?page={current_page}'
        return super().get_redirect_url(*args, **kwargs)


class AnswerSelectRightView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        current_question = Questions.objects.get(pk=pk)
        if self.request.user != current_question.author:
            return super().get_redirect_url(*args, **kwargs)
        id_answer = kwargs['id_answer']
        with transaction.atomic():
            old_correct_answer = Answers.objects.filter(correct=True).first()
            if old_correct_answer:
                old_correct_answer.correct = False
                old_correct_answer.save()
            answer = Answers.objects.get(pk=id_answer)
            answer.correct = True
            answer.save()
        current_page = self.request.GET.get('page')
        self.url = f"{reverse('questions:questionview', args=[pk])}?page={current_page}"
        return super().get_redirect_url(*args, **kwargs)

class SearchQuestionView(ListView):

    model = Questions
    paginate_by = 20
    template_name = 'questions/search_result.html'

    def get_queryset(self):
        search_string = self.request.GET.get('search')
        if search_string[:4] == 'tag:':
            queryset = Questions.objects.filter(tags__name__contains=search_string[4:]).annotate(
                count_votes=Count('questionvotes', distinct=True),
                count_answers=Count('answers', distinct=True)
            ).order_by('-count_votes', '-create_date')
        else:
            queryset = Questions.objects.filter(title_contains=search_string).annotate(
                count_votes=Count('questionvotes', distinct=True),
                count_answers=Count('answers', distinct=True)
            ).order_by('-count_votes', '-create_date')
        return queryset

    def post(self, request):
        search_string = request.POST.get('search_string')
        return redirect(f'/searchresult/?search={search_string}')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search = self.request.GET.get('search')
        context['search'] = search
        context['trends'] = Questions.get_trends()
        if self.request.user.is_authenticated:
            profile = UserProfile.objects.get(user=self.request.user)
            context['photo'] = profile.photo
        return context








