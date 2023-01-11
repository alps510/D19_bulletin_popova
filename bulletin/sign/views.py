import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from .models import OneTimeCode


def usual_login_view(request):
    email = request.POST['login']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is not None:
        code = ''.join(random.choice('abcde12345') for _ in range(5))
        if OneTimeCode.objects.filter(user=user).exists():
            OneTimeCode.objects.filter(user=user).update(code=code)
        else:
            OneTimeCode.objects.create(code=code, user=user)
        send_mail(
            subject='Код входа в систему',
            message=code,
            from_email='alps51@yandex.ru',
            recipient_list=[user.email]
        )
        return redirect('/sign/entercode')
    else:
        return HttpResponse('invalid login error')


def login_with_code_view(request):
    username = request.POST['username']
    code = request.POST['code']
    user = User.objects.get(username=username)
    if OneTimeCode.objects.filter(code=code, user__username=username).exists():
        login(request, user=user, backend='allauth.account.auth_backends.AuthenticationBackend')
        return redirect('/')
    else:
        return HttpResponse('invalid login error')


class EnterCodeView(TemplateView):
    template_name = 'sign/entercode.html'


