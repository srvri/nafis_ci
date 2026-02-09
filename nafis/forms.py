from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل شما'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'موضوع پیام'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام شما',
                'rows': 5
            })
        }
        labels = {
            'name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'subject': 'موضوع',
            'message': 'پیام'
        }