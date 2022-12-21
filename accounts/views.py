from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from .forms import UserModelForm, UserLoginForm


class UserRegistrationPageView(View):
    def get(self, request, *args, **kwargs):
        form = UserModelForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = UserModelForm(request.POST)
        if form.is_valid():
            print(form.data)
            form.save()


class UserLoginPageView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'accounts/signin.html', context)