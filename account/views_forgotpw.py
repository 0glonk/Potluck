# Forgot Password Imports
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from home.models import CustomUser
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from account import views_forgotpw

# Reset Password Imports
from django.utils.http import urlsafe_base64_decode

# ====== Forgot Password ====== #
def forgot_pw(request):
    """ Handle the forgot password process. """
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the email from the form data
        user = CustomUser.objects.filter(email=email).first()  # Find the user by email

        if user:
            # Generate a password reset token
            token = default_token_generator.make_token(user)  # Generate a token for password reset
            uid = urlsafe_base64_encode(force_bytes(user.pk))  # Encode the user ID

            # Create the password reset link
            reset_link = request.build_absolute_uri(reverse('reset_pw', kwargs={'uidb64': uid, 'token': token}))

            # Send the password reset email
            send_mail(
                'Reset your password',
                f'Click the link to reset your password: {reset_link}',
                'potlucknoreply@gmail.com',  # Replace this with your app's sender email
                [email],  # recipient_list as a list
            )

            return TemplateResponse(request, 'email_sent.html', {'email': email})  # Render a success page
    return TemplateResponse(request, 'forgot_pw.html', {})  # Render the forgot password form

# ====== Reset Password ====== #
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() # Decode the user ID
        user = CustomUser.objects.get(pk=uid) # Get the user object
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist): 
        user = None

    if request.method == 'POST':
        new_password = request.POST.get('new_password') # Get the new password from the form data
        confirm_password = request.POST.get('confirm_password') # Get the confirmation password
        if user and default_token_generator.check_token(user, token): # Check if the token is valid
            if new_password == confirm_password:
                # Validate the new password based on requirements
                is_too_short = len(new_password) < 8
                has_number = any(char.isdigit() for char in new_password)
                has_upper = any(char.isupper() for char in new_password)
                has_special = any(char in "!@#$%^&*()_+" for char in new_password)

                if is_too_short or not has_number or not has_upper or not has_special:
                    return render(request, 'reset_password.html', {
                        'uid': uidb64,
                        'token': token,
                        'error': 'Password must be at least 8 characters long, include at least one number, one uppercase letter, and one special character.'
                    })

                user.set_password(new_password)
                user.save()
                return render(request, 'reset_success.html')
            else:
                return render(request, 'reset_password.html', {
                    'uid': uidb64,
                    'token': token,
                    'error': 'Passwords do not match'
                })

    return render(request, 'reset_password.html', {'uid': uidb64, 'token': token}) # Render the reset password form if the token is invalid or expired

# ====== Resend Email Link ====== #
@csrf_exempt
def resend_email_link(request):
    """Handle resending the reset password link."""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('reset_pw', kwargs={'uidb64': uid, 'token': token}))

            send_mail(
                'Reset your password',
                f'Click the link to reset your password: {reset_link}',
                'potlucknoreply@gmail.com',
                [email],
            )

            return TemplateResponse(request, 'email_sent.html', {'email': email})
    return render(request, 'forgot_pw.html', {'error': 'Unable to resend email. Please try again.'})
