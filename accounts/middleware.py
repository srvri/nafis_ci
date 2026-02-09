# accounts/middleware.py
from django.shortcuts import redirect
from django.urls import reverse


class AuthRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # اگر کاربر لاگین است و به صفحه ورود یا ثبت‌نام می‌رود
        if request.user.is_authenticated:
            login_url = reverse('accounts:login')
            signup_url = reverse('accounts:signup')

            if request.path in [login_url, signup_url]:
                return redirect('accounts:profile')

        response = self.get_response(request)
        return response