from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .forms import (
    CustomerRegistrationForm, TraderRegistrationForm, AdminRegistrationForm,
    CustomAuthenticationForm, ProfileUpdateForm, TraderProfileUpdateForm,
    CustomerProfileUpdateForm
)
from .models import User, PasswordResetOTP
from utils.email_service import EmailNotificationService
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.utils import timezone
import json


class CustomLoginView(LoginView):
    """Custom login view with role-based authentication"""
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['role'] = self.request.GET.get('role')
        return kwargs

    def get_success_url(self):
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('adminpanel:dashboard')
        elif user.is_trader:
            return reverse_lazy('shops:trader_dashboard')
        else:
            return reverse_lazy('shops:home')


def register_customer(request):
    """Customer registration view"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Customer account created successfully! You can now login.')
            return redirect('users:login')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'users/register_customer.html', {'form': form})


def register_trader(request):
    """Trader registration view"""
    if request.method == 'POST':
        form = TraderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Trader account created successfully! Please wait for admin approval.')
            return redirect('users:login')
    else:
        form = TraderRegistrationForm()

    return render(request, 'users/register_trader.html', {'form': form})


def register_admin(request):
    """Admin registration view (restricted)"""
    # Only allow superusers to create admin accounts
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, 'You do not have permission to create admin accounts.')
        return redirect('users:login')

    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Admin account created successfully!')
            return redirect('adminpanel:dashboard')
    else:
        form = AdminRegistrationForm()

    return render(request, 'users/register_admin.html', {'form': form})


@login_required
def profile_view(request):
    """View user profile"""
    context = {
        'user': request.user,
    }

    if request.user.is_trader:
        context['trader_profile'] = getattr(request.user, 'trader_profile', None)
    elif request.user.is_customer:
        context['customer_profile'] = getattr(request.user, 'customer_profile', None)

    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, instance=request.user)

        if request.user.is_trader:
            trader_form = TraderProfileUpdateForm(
                request.POST,
                instance=getattr(request.user, 'trader_profile', None)
            )
            if user_form.is_valid() and trader_form.is_valid():
                user_form.save()
                trader_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('users:profile')
        elif request.user.is_customer:
            customer_form = CustomerProfileUpdateForm(
                request.POST,
                instance=getattr(request.user, 'customer_profile', None)
            )
            if user_form.is_valid() and customer_form.is_valid():
                user_form.save()
                customer_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('users:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('users:profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        trader_form = None
        customer_form = None

        if request.user.is_trader:
            trader_form = TraderProfileUpdateForm(
                instance=getattr(request.user, 'trader_profile', None)
            )
        elif request.user.is_customer:
            customer_form = CustomerProfileUpdateForm(
                instance=getattr(request.user, 'customer_profile', None)
            )

    context = {
        'user_form': user_form,
        'trader_form': trader_form,
        'customer_form': customer_form,
    }

    return render(request, 'users/edit_profile.html', context)


def custom_logout(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('shops:home')


def forgot_password(request):
    """Forgot password page"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'users/forgot_password.html')

        try:
            user = User.objects.get(email=email)

            # Create OTP for user
            otp = PasswordResetOTP.create_otp_for_user(user)

            # Send OTP email
            email_sent = EmailNotificationService.send_password_reset_otp_email(user, otp.otp_code)

            if email_sent:
                messages.success(request, f'A verification code has been sent to {email}. Please check your email.')
                return redirect('users:verify_otp', email=email)
            else:
                messages.error(request, 'Failed to send verification code. Please try again.')

        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            messages.success(request, f'If an account with {email} exists, a verification code has been sent.')
            return render(request, 'users/forgot_password.html')

    return render(request, 'users/forgot_password.html')


def verify_otp(request, email):
    """Verify OTP and reset password"""
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([otp_code, new_password, confirm_password]):
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'users/verify_otp.html', {'email': email})

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/verify_otp.html', {'email': email})

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'users/verify_otp.html', {'email': email})

        try:
            user = User.objects.get(email=email)

            # Find valid OTP
            otp = PasswordResetOTP.objects.filter(
                user=user,
                otp_code=otp_code,
                is_used=False
            ).first()

            if not otp:
                messages.error(request, 'Invalid verification code.')
                return render(request, 'users/verify_otp.html', {'email': email})

            if not otp.is_valid():
                if otp.is_expired():
                    messages.error(request, 'Verification code has expired. Please request a new one.')
                else:
                    messages.error(request, 'Verification code is no longer valid.')
                return redirect('users:forgot_password')

            # Increment attempts
            otp.increment_attempts()

            # Check if max attempts reached
            if otp.attempts >= otp.max_attempts:
                otp.mark_as_used()
                messages.error(request, 'Too many attempts. Please request a new verification code.')
                return redirect('users:forgot_password')

            # Reset password
            user.set_password(new_password)
            user.save()

            # Mark OTP as used
            otp.mark_as_used()

            messages.success(request, 'Password reset successfully! You can now login with your new password.')
            return redirect('users:login')

        except User.DoesNotExist:
            messages.error(request, 'Invalid request.')
            return redirect('users:forgot_password')

    return render(request, 'users/verify_otp.html', {'email': email})


@require_POST
def resend_otp(request):
    """Resend OTP via AJAX"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'})

        try:
            user = User.objects.get(email=email)

            # Create new OTP
            otp = PasswordResetOTP.create_otp_for_user(user)

            # Send OTP email
            email_sent = EmailNotificationService.send_password_reset_otp_email(user, otp.otp_code)

            if email_sent:
                return JsonResponse({
                    'success': True,
                    'message': 'New verification code sent successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Failed to send verification code. Please try again.'
                })

        except User.DoesNotExist:
            # Don't reveal if email exists or not
            return JsonResponse({
                'success': True,
                'message': 'If the email exists, a new verification code has been sent.'
            })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request format.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
