from django.test import TestCase, RequestFactory
from django.urls import reverse
from bookingandbilling.models import Customer, Interpreter, Appointment
from bookingandbilling.views.views_registration import send_reset_email
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from rest_framework.test import APIClient
from rest_framework import status
import re
from bookingandbilling.email_utils import (
    send_appointment_offered_email,
    send_appointment_accepted_email
)

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            username='testuser', 
            email='testuser@example.com',
            password='password123',
            first_name='Test', 
            last_name='User')
        self.user2 = Customer.objects.create_user(
            username='amamsamsmasms',
            email='cowcowmoo@example.com',
            password='possword',
            first_name='cow',
            last_name='moo')
        self.client = APIClient()
        self.factory = RequestFactory()
        self.token_generator = PasswordResetTokenGenerator()
        self.reset_url = reverse('send-password-reset-email')

    def test_password_reset_email(self):  
        request = self.factory.post(self.reset_url, {'email': self.user.email})
        email = send_reset_email(request, self.user)
        self.assertEqual(email.subject, 'Password Reset Request')
        self.assertEqual(email.to, [self.user.email])
        uid = urlsafe_base64_encode(force_bytes(self.user.email))
        self.assertIn(uid, email.body)
        token_match = re.search(r'/new-password/[^/]+/([^/]+)/?', email.body)
        self.assertTrue(self.token_generator.check_token(self.user, token_match.group(1)))
        
    def test_password_reset_wrong_user(self):
        request = self.factory.post(self.reset_url, {'email': self.user2.email})
        email = send_reset_email(request, self.user2)
        self.assertEqual(email.subject, 'Password Reset Request')
        self.assertEqual(email.to, [self.user2.email])
        uid = urlsafe_base64_encode(force_bytes(self.user2.email))
        self.assertIn(uid, email.body)
        token_match = re.search(r'/new-password/.+/(.+)/', email.body)
        self.assertFalse(self.token_generator.check_token(self.user, token_match.group(1)))
        
    def test_password_reset_update_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.email))
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user)
        
        data = {'password': 'newpassword123',"uidb64":uid,"token":token}
        
        response = self.client.post(reverse('update-password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))
        
    def test_password_reset_update_password_wrong_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.email))
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self.user2)
        
        data = {'password': 'newpassword123',"uidb64":uid,"token":token}
        
        response = self.client.post(reverse('update-password'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('password123'))
    
class AppointmentEmailsTestCase(TestCase):
    def setUp(self):
        self.user = Customer.objects.create_user(
            username='testuser', 
            email='testuser@example.com',
            password='password123',
            first_name='Test', 
            last_name='User')
        self.user2 = Interpreter.objects.create_user(
            username='amamsamsmasms',
            email='cowcowmoo@example.com',
            password='possword',
            first_name='cow',
            last_name='moo',
        )
        self.appointment = Appointment.objects.create(
            customer=self.user,
            interpreter=self.user2,
            planned_start_time='2025-01-24T20:00',
            planned_duration='01:00',
            location='testlocation',
            notes='testnotes'
        )

    def test_appointment_offered_email(self):
        email = send_appointment_offered_email(self.appointment, self.user2)
        self.assertEqual(email.subject, 'Appointment Offered')
        self.assertEqual(email.to, [self.user2.email])
        self.assertIn('You have Been Offered an Appointment', email.body)
        self.assertIn('testlocation', email.body)
        
    def test_appointment_accepted_email(self):
        email = send_appointment_accepted_email(self.appointment, self.user)
        self.assertEqual(email.subject, 'Appointment Accepted')
        self.assertEqual(email.to, [self.user.email])
        self.assertIn('An Interpreter has accepted your Appointment', email.body)
        self.assertIn('testlocation', email.body)
