from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import UserModelForm, UserLoginForm

User = get_user_model()


class UserRegistrationPageView(View):
    def get(self, request, *args, **kwargs):
        form = UserModelForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)

    def post(self, request, *args, **kwargs):
        form = UserModelForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(
                email = email,
                password = password
            )
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()
            messages.success(request, f'Registration Successful {email}')
            return redirect('accounts:login')


class UserLoginPageView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        context = {'form': form}
        return render(request, 'accounts/signin.html', context)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                print(f'user {email}')
                login(request, user=user)
                messages.success(request, f'{email} Successfully logged in.')
                return redirect('store:home')
            else:
                print('User is none')



class UserLogoutPageView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('store:home')