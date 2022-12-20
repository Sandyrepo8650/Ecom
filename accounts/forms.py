from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

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

