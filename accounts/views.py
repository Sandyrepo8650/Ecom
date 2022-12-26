from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from .models import User
from .forms import UserModelForm, UserLoginForm
from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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

            # email sending
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domin': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Registration Successful. Please Recieve the email to activate the account')
            return redirect('accounts:register')


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
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


class UserActivatePageView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Congratulation! Your account is activate')
            return redirect('accounts:login')
        else:
            messages.success(request, 'Invalid activation link')
            return redirect('accounts:register')


class ForgotPasswordPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'accounts/forgotpassword.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        user = User.objects.filter(email=email).exists()
        if user:
            return redirect('accounts:resetpassword')
        else:
            messages.success(request, 'User does not exists, Please enter a vaild email address')
            return redirect('accounts:forgotpassword')


class ResetPasswordPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'accounts/resetpassword.html', context)
    
    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        password1 = request.POST['password1']
        if password is not None and password != password1:
            print(password)
            exit()