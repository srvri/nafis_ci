from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signup-email/', views.signup_email, name='signup_email'),
    path('required_login/', views.Required_Login, name='required_login'),
    path('profile/', views.profile, name='profile'),
    path('check_login/', views.check_login, name='check_login'),
    path('re_path/<int:year>/', views.re_path, name='re_path'),
    path('session_fun/', views.session_fun, name='session_fun'),
    path('session_del/', views.session_del, name='session_del'),
    path('cookie_set/', views.cookie_set, name='cookie_set'),
    path('cookie_get/', views.cookie_get, name='cookie_get'),
    path('cookies_sessions/', views.cookies_sessions, name='cookies_sessions'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('verify_phone_number/', views.verify_phone_number, name='verify_phone_number'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # ویرایش پروفایل
    path('profile/change-password/', views.change_password, name='change_password'),  # تغییر رمز عبور
    path('profile/support/', views.support, name='support'),  # پشتیبانی
    path('profile/addresses/', views.addresses, name='addresses'),  # آدرس‌ها
    path('profile/orders/', views.orders, name='orders'),  # سفارشات
    path('profile/wishlist/', views.wishlist, name='wishlist'),  # علاقه‌مندی‌ها
    path('profile/notifications/', views.notifications, name='notifications'),  # اعلان‌ها
    path('wishlist/', views.wishlist, name='wishlist'),
]