from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()

class UserModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email address already exists')
        return email

    def clean_password2(self):
        password1 = self.changed_data.get('password1')
        password2 = self.changed_data.get('password2')

        if password1 is None and password1 != password2:
            raise ValidationError('Both password should be same.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        user.set_password(password1)
        user.save(using=self._db)
        return user


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=220, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))