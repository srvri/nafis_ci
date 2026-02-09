from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse_lazy
from .forms import UserForm, UserRegistrationForm, EmailRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
import random
import re
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile, Address, Wishlist
from django import forms

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            request.session['form_data'] = {
                'email': '',  # Keep email empty for phone signup; user can fill it in profile later
                'password': form.cleaned_data['password'],
                'phone_number': form.cleaned_data['phone_number'],
            }
            send_verification_code(request, phone_number, is_phone=True)
            return redirect('accounts:verify_phone_number')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form[field].label}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/sign-up.html', {'form': form})

def signup_email(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == "POST":
        form = EmailRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['form_data'] = {
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password'],
                'phone_number': '',
            }
            send_verification_code(request, email, is_phone=False)
            return redirect('accounts:verify_email')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form[field].label}: {error}")
    else:
        form = EmailRegistrationForm()
    return render(request, 'accounts/sign-up-email.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email_or_phone = form.cleaned_data.get('email_or_phone')
            password = form.cleaned_data['password']
            user = None
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            phone_regex = r'^09\d{9}$'
            
            if re.match(email_regex, email_or_phone):
                # Try to find user by email (check User.email or UserProfile.email)
                try:
                    user = User.objects.get(email=email_or_phone)
                except User.DoesNotExist:
                    try:
                        user_profile = UserProfile.objects.get(email=email_or_phone)
                        user = user_profile.user
                    except UserProfile.DoesNotExist:
                        user = None
                        
            elif re.match(phone_regex, email_or_phone):
                # Phone number: try both User.username (clean phone) and UserProfile.phone_number
                try:
                    user = User.objects.get(username=email_or_phone)
                except User.DoesNotExist:
                    try:
                        user_profile = UserProfile.objects.get(phone_number=email_or_phone)
                        user = user_profile.user
                    except UserProfile.DoesNotExist:
                        user = None
            else:
                messages.error(request, "ایمیل یا شماره تلفن معتبر نیست.")
                
            if user:
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "با موفقیت وارد شدید. خوش آمدید!")
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('accounts:profile')
                else:
                    messages.error(request, "رمز عبور اشتباه است.")
            else:
                messages.error(request, "ایمیل یا شماره تلفن یافت نشد.")
    else:
        form = UserForm()
    return render(request, 'accounts/sign-in.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('nafis:index')

def forgot_password(request):
    """View for forgot password - accepts email or phone number"""
    if request.method == "POST":
        email_or_phone = request.POST.get('email_or_phone', '').strip()
        
        if not email_or_phone:
            messages.error(request, "لطفاً ایمیل یا شماره تلفن را وارد کنید.")
            return render(request, 'accounts/forgot_password.html')
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_regex = r'^09\d{9}$'
        
        if re.match(email_regex, email_or_phone):
            # Email verification
            request.session['reset_email'] = email_or_phone
            send_verification_code(request, email_or_phone, is_phone=False)
            return redirect('accounts:verify_email')
        
        elif re.match(phone_regex, email_or_phone):
            # Phone verification
            request.session['reset_phone'] = email_or_phone
            send_verification_code(request, email_or_phone, is_phone=True)
            return redirect('accounts:verify_phone_number')
        
        else:
            messages.error(request, "ایمیل یا شماره تلفن معتبر نیست.")
    
    return render(request, 'accounts/forgot_password.html')

def reset_password(request):
    """View to set new password after verification"""
    email_verified = request.session.get('email_verified')
    phone_verified = request.session.get('phone_verified')
    reset_email = request.session.get('reset_email')
    reset_phone = request.session.get('reset_phone')
    
    # Check if user came from verification
    if not (email_verified or phone_verified):
        messages.error(request, "لطفاً ابتدا ایمیل یا شماره تلفن خود را تأیید کنید.")
        return redirect('accounts:forgot_password')
    
    if request.method == "POST":
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()
        
        if not password1 or not password2:
            messages.error(request, "لطفاً هر دو فیلد رمز عبور را پر کنید.")
            return render(request, 'accounts/reset_password.html')
        
        if password1 != password2:
            messages.error(request, "رمزهای عبور مطابقت ندارند.")
            return render(request, 'accounts/reset_password.html')
        
        if len(password1) < 8:
            messages.error(request, "رمز عبور باید حداقل 8 کاراکتر باشد.")
            return render(request, 'accounts/reset_password.html')
        
        # Find user by email or phone
        user = None
        if email_verified and reset_email:
            try:
                user = User.objects.get(email=reset_email)
            except User.DoesNotExist:
                try:
                    user_profile = UserProfile.objects.get(email=reset_email)
                    user = user_profile.user
                except UserProfile.DoesNotExist:
                    user = None
        
        elif phone_verified and reset_phone:
            try:
                user = User.objects.get(username=reset_phone)
            except User.DoesNotExist:
                try:
                    user_profile = UserProfile.objects.get(phone_number=reset_phone)
                    user = user_profile.user
                except UserProfile.DoesNotExist:
                    user = None
        
        if user:
            user.set_password(password1)
            user.save()
            
            # Clear session
            request.session.pop('email_verified', None)
            request.session.pop('phone_verified', None)
            request.session.pop('reset_email', None)
            request.session.pop('reset_phone', None)
            request.session.pop('verification_code', None)
            
            messages.success(request, "رمز عبور شما با موفقیت تغییر کرد. اکنون وارد شوید.")
            return redirect('accounts:login')
        else:
            messages.error(request, "کاربر یافت نشد. لطفاً دوباره تلاش کنید.")
    
    return render(request, 'accounts/reset_password.html')

@login_required(login_url=reverse_lazy("accounts:login"))
def Required_Login(request):
    return render(request, 'accounts/required_login.html')

@login_required(login_url='accounts:login')
def profile(request):
    user = request.user

    # Handle form submission from profile page
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        gender_val = request.POST.get('gender', '').strip()

        # Ensure UserProfile exists
        if hasattr(user, 'userprofile'):
            profile = user.userprofile
        else:
            try:
                profile = UserProfile.objects.create(user=user)
            except Exception:
                profile = None

        # Save ALL fields to UserProfile (primary storage location)
        if profile:
            if first_name != '':
                profile.first_name = first_name
            if last_name != '':
                profile.last_name = last_name
            if email != '':
                profile.email = email
            if phone != '':
                profile.phone_number = phone
            if birth_date:
                try:
                    from datetime import datetime
                    profile.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                except Exception:
                    pass
            # Normalize gender values (template uses 'F'/'M')
            if gender_val in ['M', 'm', 'male', 'Male']:
                profile.gender = 'male'
            elif gender_val in ['F', 'f', 'female', 'Female']:
                profile.gender = 'female'
            elif gender_val:
                profile.gender = 'other'

            profile.save()

        messages.success(request, "اطلاعات با موفقیت ذخیره شد.")
        return redirect('accounts:profile')

    # GET: show profile
    user_profile = getattr(user, 'userprofile', None)
    # attach attribute `profile` on user so templates using `user.profile` work
    setattr(user, 'profile', user_profile)
    addresses = Address.objects.filter(user=user_profile) if user_profile and 'Address' in globals() else []
    orders = []  # اینجا باید از مدل سفارشات استفاده کنید
    return render(request, 'accounts/profile.html', {'user_profile': user_profile, 'addresses': addresses, 'orders': orders})

@login_required(login_url='accounts:login')
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user.userprofile if hasattr(request.user, 'userprofile') else None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "حساب کاربری شما با موفقیت تکمیل شد.")
            return redirect('accounts:profile')
    else:
        form = EditProfileForm(instance=request.user.userprofile if hasattr(request.user, 'userprofile') else None)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required(login_url='accounts:login')
@login_required(login_url='accounts:login')
def change_password(request):
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # حفظ جلسه پس از تغییر رمز
            messages.success(request, "رمز عبور شما با موفقیت تغییر کرد.")
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form, 'user_profile': user_profile})

@login_required(login_url='accounts:login')
@login_required(login_url='accounts:login')
def support(request):
    from .models import SupportMessage
    
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    support_messages = []
    
    if request.method == "POST":
        message_text = request.POST.get('message', '').strip()
        if message_text and user_profile:
            # ذخیره پیام در دیتابیس
            SupportMessage.objects.create(
                user=user_profile,
                message=message_text
            )
            messages.success(request, "پیام شما با موفقیت ارسال شد.")
            return redirect('accounts:support')
        elif not message_text:
            messages.error(request, "لطفاً پیام خود را وارد کنید.")
        else:
            messages.error(request, "خطا: پروفایل کاربری یافت نشد.")
    
    # دریافت تمام پیام‌های کاربر فعلی
    if user_profile:
        support_messages = SupportMessage.objects.filter(user=user_profile).order_by('-created_at')
    
    return render(request, 'accounts/support.html', {
        'user_profile': user_profile,
        'support_messages': support_messages
    })

@login_required(login_url='accounts:login')
def addresses(request):
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user_profile
            address.save()
            messages.success(request, "آدرس شما با موفقیت ثبت شد.")
            return redirect('accounts:addresses')
    else:
        form = AddressForm()
    addresses = Address.objects.filter(user=user_profile) if user_profile else []
    return render(request, 'accounts/addresses.html', {'form': form, 'addresses': addresses, 'user_profile': user_profile})

@login_required(login_url='accounts:login')
def orders(request):
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    orders = []  # اینجا باید از مدل سفارشات استفاده کنید
    return render(request, 'accounts/orders.html', {'orders': orders, 'user_profile': user_profile})

@login_required(login_url='accounts:login')
def wishlist(request):
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    wishlist_items = Wishlist.objects.filter(user=user_profile) if user_profile else []
    return render(request, 'accounts/wishlist.html', {'wishlist_items': wishlist_items, 'user_profile': user_profile})


@login_required(login_url='accounts:login')
def notifications(request):
    """Simple notifications view: returns a list (empty by default).

    If you add a Notification model later, replace the empty list with a query
    like: Notification.objects.filter(user=request.user).order_by('-timestamp')
    """
    user_profile = request.user.userprofile if hasattr(request.user, 'userprofile') else None
    notifications = []
    # Attempt to use a Notification model if it exists
    try:
        from .models import Notification
    except Exception:
        Notification = None

    if Notification:
        try:
            notifications = Notification.objects.filter(user=user_profile).order_by('-timestamp') if user_profile else []
        except Exception:
            notifications = []

    return render(request, 'accounts/notifications.html', {'notifications': notifications, 'user_profile': user_profile})

def check_login(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    else:
        return redirect('accounts:login')

from datetime import datetime

def re_path(request, year):
    return HttpResponse("the year is " + str(year))

def session_fun(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return HttpResponse("num of visit is " + str(num_visits))

def session_del(request):
    try:
        del request.session["num_visits"]
    except KeyError:
        pass
    return HttpResponse("session deleted")

def cookie_set(request):
    response = HttpResponse("cookie_set")
    if request.COOKIES.get('last_visit'):
        visits = int(request.COOKIES.get('visit'))
        last_visit = request.COOKIES['last_visit']
        last_visit_time = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - last_visit_time).seconds > 20:
            response.set_cookie('visit', visits + 1)
            response.set_cookie('last_visit', datetime.now())
    else:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visit', 0)
    return response

def cookie_get(request):
    massage = "number of visits is " + str(request.COOKIES.get('visit')) + " and last visit is : " + str(request.COOKIES.get('last_visit'))
    return HttpResponse(massage)

def cookies_sessions(request):
    num_visits = request.session.get('num_visits', 0)
    cookie_visits = request.COOKIES.get('visit', 0)
    last_visit = request.COOKIES.get('last_visit', 'No last visit recorded')
    return render(request, 'cookies_sessions.html', {'num_visits': num_visits, 'cookie_visits': cookie_visits, 'last_visit': last_visit})

def send_verification_code(request, contact, is_phone=False):
    subject = 'تولیدی پوشاک نفیس - کد تایید'
    # برای development: از کد ثابت استفاده می‌کنیم
    verification_code = '1234'  # کد development
    
    if is_phone:
        message = f'سلام و درود، کد تایید شما برای ثبت‌نام در تولیدی پوشاک نفیس: {verification_code}\n(توجه: در حالت توسعه، هر کدی قابل قبول است)'
        print(f"Verification code for {contact}: {verification_code}")
    else:
        message = f'سلام و درود، کد تایید شما برای ثبت‌نام در تولیدی پوشاک نفیس: {verification_code}\n(توجه: در حالت توسعه، هر کدی قابل قبول است)'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [contact]
        res = send_mail(subject, message, email_from, recipient_list)
        if res != 1:
            messages.error(request, "خطا در ارسال ایمیل")
            return HttpResponse("خطا در ارسال ایمیل")
    request.session['verification_code'] = verification_code
    request.session['verification_contact'] = contact
    messages.info(request, f"کد تایید: {verification_code} (حالت توسعه - هر کدی قابل قبول است)")
    return HttpResponse("کد با موفقیت ارسال شد")

def verify_email(request):
    if request.method == "POST":
        code = request.POST.get('verification_code')
        session_code = request.session.get('verification_code')
        
        # برای development: هر کد را قبول کن
        if str(code).strip():  # فقط بررسی کنید که کد خالی نیست
            # Check if this is for password reset
            reset_email = request.session.get('reset_email')
            if reset_email:
                # Password reset flow
                request.session.pop('verification_code', None)
                request.session.pop('verification_contact', None)
                request.session['email_verified'] = True
                messages.success(request, "ایمیل شما تأیید شد. اکنون می‌توانید رمز عبور جدید را تنظیم کنید.")
                return redirect('accounts:reset_password')
            
            # Signup flow
            form_data = request.session.get('form_data')
            if form_data:
                # Use email as username for email-signup users
                username = form_data['email']
                user = User.objects.create_user(
                    username=username,
                    email=form_data['email'],
                    password=form_data['password'],
                )
                UserProfile.objects.create(
                    user=user,
                    phone_number=form_data['phone_number'],
                    email=form_data['email']
                )
                request.session.pop('verification_code', None)
                request.session.pop('verification_contact', None)
                request.session.pop('form_data', None)
                messages.success(request, "ثبت‌نام شما با موفقیت انجام شد! خوش آمدید.")
                return redirect('accounts:login')
            else:
                messages.error(request, "خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.")
        else:
            messages.error(request, "لطفاً کد تأیید را وارد کنید.")
    return render(request, 'accounts/verify_email.html')

def verify_phone_number(request):
    if request.method == "POST":
        code = request.POST.get('verification_code')
        session_code = request.session.get('verification_code')
        
        # برای development: هر کد را قبول کن
        if str(code).strip():  # فقط بررسی کنید که کد خالی نیست
            # Check if this is for password reset
            reset_phone = request.session.get('reset_phone')
            if reset_phone:
                # Password reset flow
                request.session.pop('verification_code', None)
                request.session.pop('verification_contact', None)
                request.session['phone_verified'] = True
                messages.success(request, "شماره تلفن شما تأیید شد. اکنون می‌توانید رمز عبور جدید را تنظیم کنید.")
                return redirect('accounts:reset_password')
            
            # Signup flow
            form_data = request.session.get('form_data')
            if form_data:
                # Use phone number (09XXXXXXXXX) as username, NOT the @phone.example.com email
                phone_number = form_data['phone_number']
                user = User.objects.create_user(
                    username=phone_number,  # Clean: just the phone number
                    email=form_data['email'],
                    password=form_data['password'],
                )
                UserProfile.objects.create(
                    user=user,
                    phone_number=phone_number,
                    email=form_data['email']
                )
                request.session.pop('verification_code', None)
                request.session.pop('verification_contact', None)
                request.session.pop('form_data', None)
                messages.success(request, "ثبت‌نام شما با موفقیت انجام شد! خوش آمدید.")
                return redirect('accounts:login')
            else:
                messages.error(request, "خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.")
        else:
            messages.error(request, "لطفاً کد تأیید را وارد کنید.")
    return render(request, 'accounts/verify_phone_number.html')

# فرم‌های جدید
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date', 'gender']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'dir': 'rtl'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'dir': 'rtl'}),
        }

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='رمز عبور فعلی'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='رمز عبور جدید'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='تأیید رمز عبور جدید'
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("رمزهای عبور جدید مطابقت ندارند.")
        return cleaned_data

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('رمز عبور فعلی اشتباه است.')
        return old_password

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
        return self.user

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'phone_number', 'address', 'postal_code', 'city']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'dir': 'rtl'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        }
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'phone_number': 'شماره تلفن',
            'address': 'آدرس',
            'postal_code': 'کد پستی',
            'city': 'شهر',
        }