# Default Imports
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from home.models import CustomUser

# Login/Out
from django.contrib.auth import logout as django_logout
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from .forms import SignUpForm

# Email imports
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.contrib.auth.models import User

# Email verification imports
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Login connection stuff -AJ
def login_view(request):
    """ Log in the user and redirect to the home page. """
    print("login_view triggered")

    if request.method == 'POST':
        if request.POST.get('email') == '' or request.POST.get('password') == '':
            return TemplateResponse(request, 'login.html', {
                'error': 'Please enter both email and password.'
            })
        
        email = request.POST.get('email')  
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print("Authenticated user:", user)

        if user is not None:
            if user.is_active:
                django_login(request, user)
                return redirect('/')
            else:
                return TemplateResponse(request, 'login.html', {
                    'error': 'Please verify your email before logging in.'
                })
        else:
            return TemplateResponse(request, 'login.html', {
                'error': 'Invalid email or password'
            })

    return TemplateResponse(request, 'login.html', {})

# Log out connection stuff -AJ
@login_required
def logout_view(request):
    """ Log out the user and redirect to the home page. """
    print("logout_view triggered")  # For debugging
    django_logout(request)          # To end the session
    return redirect('home')         # Redirect to home page after logout

@login_required
def logout_page(request):
    """ Logout pop-up """
    return TemplateResponse(request, 'logout.html', {})  # renders the "You have been logged out" message

# ====== Signup ====== #

from django.db import IntegrityError
from django.urls import reverse

def sign_up(request):
    if request.method == 'POST':
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        # Check if email or username already exist
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'sign_up.html', {
                'form': SignUpForm(),
                'error': 'An account with this email already exists.'
            })

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'sign_up.html', {
                'form': SignUpForm(),
                'error': 'This username is already taken.'
            })
        
        # Check if password is strong enough - Daniel 
        is_too_short = len(password) < 8 
        has_number = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)           # Check for uppercase letters
        has_special = any(char in "!@#$%^&*()_+" for char in password) # Check for special characters

        if is_too_short or not has_number or not has_upper or not has_special:
            return render(request, 'sign_up.html', {
                'form': SignUpForm(),
                'error': 'Password must be at least 8 characters long, include at least one number and at least one special character.'
            })

        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstName,
                last_name=lastName
            )
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = request.build_absolute_uri(reverse('verify_email', kwargs={'uidb64': uid, 'token': token}))

            send_mail(
                'Verify your email',
                f'Click the link to verify your email: {verification_link}',
                'potlucknoreply@gmail.com',
                [email],
                fail_silently=False,
            )

            return render(request, 'sign_up_success.html', {'email': email})

        except IntegrityError:
            return render(request, 'sign_up.html', {
                'form': SignUpForm(),
                'error': 'An error occurred while creating the account. Please try again.'
            })

    return render(request, 'sign_up.html', {'form': SignUpForm()})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'email_verify_success.html')
    else:
        return HttpResponse('Invalid or expired verification link.')
        
def email_verify_success(request):
    """ Email verification success page """
    return TemplateResponse(request, 'email_verify_success.html', {})  # renders the "You have been logged out" message