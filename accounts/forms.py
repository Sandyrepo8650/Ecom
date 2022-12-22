from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()

class UserModelForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number',  'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
            'phone_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
            }),

        }

        # def __init__(self, *args, **kwargs):
        #     super(UserModelForm, self).__init__(*args, **kwargs)
        #     self.fields['first_name'].widgets.attrs['placeholder'] = 'First Name'
        #     self.fields['last_name'].widgets.attrs['placeholder'] = 'Last Name'
        #     self.fields['phone_number'].widgets.attrs['placeholder'] = 'Phone Num'
        #     for field in self.fields:
        #         field[field].widgets.attrs['class'] = 'form-control'


    def clean_password2(self):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 is None and password1 != password2:
            raise ValidationError('Both password should be same.')
        return password2


class UserLoginForm(forms.Form):
    email = forms.CharField(max_length=220, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))