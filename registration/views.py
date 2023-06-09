from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView, FormView

from questions.models import Questions
from registration.forms import UserForm, UserProfileForm
from registration.models import UserProfile


class Login(LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trends'] = Questions.get_trends()
        return context

class Logout(LogoutView):
    next_page = '/'


class CreateUserView(CreateView):
    form_class = UserForm
    template_name = 'registration/create_user.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trends'] = Questions.get_trends()
        return context

    def form_valid(self, form):
        self.object = form.save()
        profile = UserProfile.objects.create(user=self.object, photo=form.cleaned_data['photo'])
        profile.save()
        return super().form_valid()

class EditProfileView(FormView):
    template_name = 'registration/edit_profile.html'
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {}
        photo_url = None
        if self.request.user.is_authenticated:
            data['login'] = self.request.user.username
            data['email'] = self.request.user.email
            profile = UserProfile.objects.filter(user=self.request.user)
            if profile is not None:
                photo_url = profile[0].photo.url
        context['form'] = UserProfileForm(initial=data)
        context['photo_url'] = photo_url
        context['trends'] = Questions.get_trends()
        return context

    def form_valid(self, form):
        renewal = False
        email = form.cleaned_data['email']
        if email != self.request.user.email:
            self.request.user.email = email
            self.request.user.save()
            renewal = True
        photo = form.cleaned_data['photo']
        if photo:
            profile = UserProfile.objects.get(user=self.request.user)
            profile.photo = photo
            profile.save()
            renewal = True
        context = self.get_context_data()
        if renewal:
            context['success'] = 'Профиль обновлен'
        else:
            context['important'] = 'Данные для обновления отсутствуют'
        return render(self.request, self.template_name, context)




