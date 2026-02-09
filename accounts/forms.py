# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput, EmailInput
from django.core.exceptions import ValidationError
import re
from .models import UserProfile  # اضافه کردن import

class UserForm(forms.Form):
    email_or_phone = forms.CharField(
        max_length=150,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل یا شماره تلفن',
            'autocomplete': 'off',
            'dir': 'rtl'
        }),
        label='ایمیل یا شماره تلفن'
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور',
            'autocomplete': 'off',
            'dir': 'rtl'
        }),
        label='رمز عبور'
    )

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data['email_or_phone']
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^09\d{9}$'
        if not (re.match(email_regex, email_or_phone) or re.match(phone_regex, email_or_phone)):
            raise ValidationError("لطفاً یک ایمیل معتبر یا شماره تلفن با فرمت 09xxxxxxxxx وارد کنید.")
        return email_or_phone

class UserRegistrationForm(forms.Form):
    phone_number = forms.CharField(
        max_length=11,
        widget=TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره تلفن',
            'autocomplete': 'off',
            'dir': 'rtl'
        }),
        label='شماره تلفن'
    )
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور',
            'autocomplete': 'off',
            'dir': 'rtl'
        }),
        label='رمز عبور'
    )

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not re.match(r'^09\d{9}$', phone):
            raise ValidationError("شماره تلفن باید با 09 شروع شود و 11 رقم باشد.")
        if UserProfile.objects.filter(phone_number=phone).exists():
            raise ValidationError("این شماره تلفن قبلاً ثبت شده است.")
        return phone

class EmailRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور',
            'autocomplete': 'off',
            'dir': 'rtl'
        }),
        label='رمز عبور'
    )

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس ایمیل',
                'autocomplete': 'off',
                'dir': 'rtl'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user