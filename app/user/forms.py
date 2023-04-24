from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

from user.models import Feedback
from user.tasks import send_reset_password_email_async


class RegisterForm(UserCreationForm):
    email = forms.EmailField(help_text='Требуется для восстановления пароля в случае утраты')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        context['user'] = context['user'].id
        send_reset_password_email_async.delay(subject_template_name=subject_template_name,
                                              email_template_name=email_template_name, context=context,
                                              from_email=from_email, to_email=to_email,
                                              html_email_template_name=html_email_template_name)


class FeedbackForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', help_text='Маскимальная длина - 50 символов')
    text = forms.CharField(widget=forms.Textarea, label='Текст', help_text='Маскимальная длина - 500 символов')

    class Meta:
        model = Feedback
        fields = ['title', 'text']
