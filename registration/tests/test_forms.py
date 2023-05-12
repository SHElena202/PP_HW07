from unittest import TestCase

from registration.forms import UserForm, UserProfileForm


class UserFormTest(TestCase):

    def test_user_form_login_label(self):
        form = UserForm()
        self.assertEqual(form.fields['username'].label, 'Имя пользователя')

    def test_user_form_password1_label(self):
        form = UserForm()
        self.assertEqual(form.fields['password1'].label, 'Пароль')

    def test_user_form_password2_label(self):
        form = UserForm()
        self.assertEqual(form.fields['password2'].label, 'Подтверждение пароля')

    def test_user_form_email_label(self):
        form = UserForm()
        self.assertEqual(form.fields['email'].label, 'Адрес электронной почты')

    def test_user_form_photo_label(self):
        form = UserForm()
        self.assertEqual(form.fields['photo'].label, 'Картинка пользователя')

class UserProfileFormTest(TestCase):

    def test_user_profile_login_label(self):
        form = UserProfileForm()
        self.assertEqual(form.fields['login'].label, 'Логин')

    def test_user_profile_photo_label(self):
        form = UserProfileForm()
        self.assertEqual(form.fields['photo'].label, 'Картинка пользователя')



