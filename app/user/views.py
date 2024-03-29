from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from user import forms


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'Вы уже авторизованы')
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Вы успешно вошли')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Введите правильное имя пользователя или пароль')
            return HttpResponseRedirect('/accounts/login')
    else:
        if request.GET.get('next'):
            messages.success(request, 'Сначала авторизуйтесь')
        context = {
            'title': 'Авторизация',
            'form': AuthenticationForm
        }
        return render(request, 'user/login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'Вы уже авторизованы')
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
            login(request, new_user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect('/')
        else:
            context = {
                'title': 'Регистрация',
                'form': form
            }
            return render(request, 'user/register.html', context)
    else:
        context = {
            'title': 'Регистрация',
            'form': forms.RegisterForm
        }
        return render(request, 'user/register.html', context)


@login_required
def profile_view(request):
    context = {
        'title': 'Профиль'
    }
    return render(request, 'user/profile.html', context)


@login_required
def logout_view(request):
    logout(request)
    context = {
        'title': 'Выход'
    }
    messages.success(request, 'Вы успешно вышли')
    return render(request, 'user/logout.html', context)


@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = forms.FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            form.save_m2m()
            messages.success(request, 'Сообщение успешно отправлено')
        else:
            messages.error(request, 'Форма не прошла валидацию')
        return HttpResponseRedirect('/feedback')
    else:
        context = {
            'title': 'Обратная связь',
            'form': forms.FeedbackForm
        }
        return render(request, 'user/feedback.html', context)