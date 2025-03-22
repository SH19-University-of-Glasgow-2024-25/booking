from django.test import TestCase, RequestFactory
from django.core import mail
from bookingandbilling.views.views_registration import send_validation_email, check_email_validation
from bookingandbilling.models import Customer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from bookingandbilling.tokens import account_activation_token


class emailTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

    def test_email_send_customer(self):

        self.customer = Customer.objects.create(
            first_name="Booking",
            last_name="Billing",
            email="bookingandbillingtest0@example.com",
            approved=False,
            address="123 Fake Street",
            postcode="Q12 WER"
        )

        request = self.factory.get('account_type')
        request.user = self.customer

        self.assertEqual(len(mail.outbox), 0)

        email = send_validation_email(request, self.customer)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(email.subject, "Account Validation")
        self.assertEqual(email.content_subtype, "html")
        self.assertEqual(email.to, ["bookingandbillingtest0@example.com"])
   
    def test_email_checking_customer(self):

        self.customer = Customer.objects.create(
            first_name="Booking",
            last_name="Billing",
            email="bookingandbillingtest0@gmail.com",
            approved=False,
            address="123 Fake Street",
            postcode="Q12 WER"
        )

        request = self.factory.get('account_type')
        request.user = self.customer

        real_uid = urlsafe_base64_encode(force_bytes(request.user.email))
        token = account_activation_token.make_token(request.user)
        response = check_email_validation(request, real_uid, token)

        self.customer.refresh_from_db()

        self.assertTrue(request.user.email_validated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Thank you for verifying your email! \
                Admins will now review your account request.")

    def test_email_checking_customer_fake_uid(self):

        self.customer = Customer.objects.create(
            first_name="Booking",
            last_name="Billing",
            email="bookingandbillingtest0@gmail.com",
            approved=False,
            address="123 Fake Street",
            postcode="Q12 WER"
        )

        request = self.factory.get('account_type')
        request.user = self.customer

        fake_uid = urlsafe_base64_encode(force_bytes("e@mail.com"))
        token = account_activation_token.make_token(request.user)
        response = check_email_validation(request, fake_uid, token)

        self.customer.refresh_from_db()

        self.assertFalse(request.user.email_validated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Oops. Something went wrong!")

    def test_email_checking_customer_non_uid(self):

        self.customer = Customer.objects.create(
            first_name="Booking",
            last_name="Billing",
            email="bookingandbillingtest0@gmail.com",
            approved=False,
            address="123 Fake Street",
            postcode="Q12 WER"
        )

        request = self.factory.get('account_type')
        request.user = self.customer
        
        non_uid = 123
        token = account_activation_token.make_token(request.user)
        response = check_email_validation(request, non_uid, token)

        self.customer.refresh_from_db()

        self.assertFalse(request.user.email_validated)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Oops. Something went wrong!")