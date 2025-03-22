from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from email.mime.image import MIMEImage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
import os


def send_validation_email(request, user):
    if user.email_validated is not True:

        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.email))

        verification_url = request.build_absolute_uri(reverse(
            'check_email_validation',
            kwargs={'uidb64':uid, 'token':token}))
            
        subject = "Account Validation"
        message = render_to_string('user/verification_email.html', {
                    'first_name': user.first_name,
                    'url' : verification_url
                })

    email = send_email(user, subject, message) 
    return email
    
    
def send_reset_email(request, user):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.email))

    verification_url = request.build_absolute_uri(reverse(
        'new-password',
        kwargs={'uidb64': uid, 'token': token}
    ))

    subject = "Password Reset Request"
    message = render_to_string('user/password_reset_email.html', {
        'first_name': user.first_name,
        'url': verification_url
    })

    email = send_email(user, subject, message) 
    return email


def send_appointment_accepted_email(appointment, customer):
    url = reverse("login")
    subject = "Appointment Accepted"
    message = render_to_string('user/appointment_accepted_email.html', {
        'first_name': customer.first_name,
        'url': url,
        'appointment_date': appointment.planned_start_time,
        'appointment_time': appointment.planned_duration,
        'language': appointment.language,
        'Interpreter': appointment.interpreter,
        'location': appointment.location,
    })

    email = send_email(customer, subject, message) 
    return email
    
def send_appointment_offered_email(appointment, interpreter):
    url = reverse("login")
    subject = "Appointment Offered"
    message = render_to_string('user/appointment_offered_email.html', {
        'first_name': interpreter.first_name,
        'url': url,
        'appointment_date': appointment.planned_start_time,
        'appointment_time': appointment.planned_duration,
        'language': appointment.language,
        'location': appointment.location,
    })

    email = send_email(interpreter, subject, message) 
    return email

def send_email(user, subject, message):
    email = EmailMultiAlternatives(subject, message, to=[user.email])
    email.content_subtype = "html"

    image_path = os.path.join(settings.BASE_DIR, 'static', 'company_logo.png')
    with open(image_path, 'rb') as img:
        image = MIMEImage(img.read())
        image.add_header('Content-ID', '<logo>')
        image.add_header('Content-Disposition', 'inline')
        email.attach(image)
    email.send()
    return email