from django.utils import timezone
from datetime import datetime, time
from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from bookingandbilling.models import Admin, Appointment, Customer, Interpreter, Language
import json

class BaseTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        self.admin = Admin.objects.create(email="johnbrown@gmail.com")
        
        self.interpreter_offered = Interpreter.objects.create(
            email="multilingualinterpreter@gmail.com")
        self.interpreter_unoffered = Interpreter.objects.create(
            email="wowza@gmail.com")

        self.customer = Customer.objects.create(
            first_name="Yogi",
            last_name="Bear",
            email="picnicbaskets@jellystone.com"
        )

        self.spanish = Language.objects.create(language_name="Spanish")

        self.appointment_assigned = Appointment.objects.create(
            customer=self.customer,
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30),
            location="Glasgow",
            language=self.spanish,
            interpreter=self.interpreter_offered,
            invoice_generated=True,
        )

        self.appointment_unassigned_1 = Appointment.objects.create(
            customer=self.customer,
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30),
            location="Glasgow",
            language=self.spanish
        )

        self.appointment_unassigned_2 = Appointment.objects.create(
            customer=self.customer,
            planned_start_time=timezone.make_aware(datetime(2024,12,1,9,0)),
            planned_duration=time(1,30),
            location="Glasgow",
            language=self.spanish
        )

        self.valid_token, _created = Token.objects.get_or_create(user=self.admin)
        self.invalid_token, _created = Token.objects.get_or_create(user=self.interpreter_offered)

        self.appointment_unassigned_1.offered_to.add(self.interpreter_offered)

class TestFetchAppointments(BaseTestCase):
    """
    
    Test fetching appointments from backend

    test_invalid_tokens: test trying to fetch appointments without valid auth
    test_fetch_assigned_appointments: test fetching assigned appointments
    test_fetch_unassigned_appointments: test fetching unassigned appointments
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/fetch-appointments/"

    def test_invalid_tokens(self):
        # no token
        response = self.client.post(self.url, {"unassigned" : True})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.post(self.url, {"unassigned" : True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fetch_assigned_appointments(self):
        self.client.cookies["authToken"] = self.valid_token
        response = self.client.post(
            self.url, json.dumps({"unassigned": False}), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        ids = [appointment['id'] for appointment in response.data["result"]]
        self.assertIn(self.appointment_assigned.id, ids)
        self.assertNotIn(self.appointment_unassigned_1.id, ids)
        self.assertNotIn(self.appointment_unassigned_2.id, ids)

    def test_fetch_unassigned_appointments(self):
        self.client.cookies["authToken"] = self.valid_token
        response = self.client.post(
            self.url, json.dumps({"unassigned": True}), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        ids = [appointment['id'] for appointment in response.data["result"]]
        self.assertIn(self.appointment_unassigned_1.id, ids)
        self.assertIn(self.appointment_unassigned_2.id, ids)
        self.assertNotIn(self.appointment_assigned.id, ids)

class TestFetchInterpreters(BaseTestCase):
    """
    
    Test fetching interpreters from backend

    test_invalid_tokens: test trying to fetch interpreters without valid auth
    test_fetch_interpreters: test fetching all interpreters
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/all-interpreters/"

    def test_invalid_tokens(self):
        # no token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fetch_interpreters(self):
        self.client.cookies["authToken"] = self.valid_token
        response = self.client.get(self.url)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        ids = [appointment['id'] for appointment in response.data["result"]]
        self.assertIn(self.interpreter_offered.id, ids)
        self.assertIn(self.interpreter_unoffered.id, ids)

class TestOfferAppointment(BaseTestCase):
    """
    
    Test offering appointments to interpreters

    test_invalid_tokens: test trying to offer appointment to interpreter without valid auth
    test_offering_appointment: test offer appointment to interpreter
    test_unoffering_appointment: test unoffer appointment to interpreter
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/offer-appointments/"

    def test_invalid_tokens(self):
        # no token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offering_appointment(self):
        self.client.cookies["authToken"] = self.valid_token
        request_data = {
            "appID":self.appointment_unassigned_1.id,
            "interpreterID":self.interpreter_unoffered.id,
            "offer":True
        }

        self.assertFalse(self.appointment_unassigned_1.offered_to.filter(
            id=self.interpreter_unoffered.id).exists())

        response = self.client.post(
            self.url, json.dumps(request_data), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.appointment_unassigned_1.offered_to.filter(
            id=self.interpreter_unoffered.id).exists())

    def test_unoffering_appointment(self):
        self.client.cookies["authToken"] = self.valid_token
        request_data = {
            "appID":self.appointment_unassigned_1.id,
            "interpreterID":self.interpreter_offered.id,
            "offer":False
        }

        self.assertTrue(self.appointment_unassigned_1.offered_to.filter(
            id=self.interpreter_offered.id).exists())

        response = self.client.post(
            self.url, json.dumps(request_data), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.appointment_unassigned_1.offered_to.filter(
            id=self.interpreter_offered.id).exists())

class TestFlaggingInvoiceGenerated(BaseTestCase):
    """
    
    Test flagging invoice generated on appointments

    test_invalid_tokens: test trying to offer appointment to interpreter without valid auth
    test_flag_invoice: test flagging invoice generated on an appointment
    test_unflag_invoice: test unflagging invoice generated on an appointment
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/toggle-appointment-invoice/"

    def test_invalid_tokens(self):
        # no token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_flag_invoice(self):
        self.client.cookies["authToken"] = self.valid_token

        self.assertFalse(self.appointment_unassigned_1.invoice_generated)

        response = self.client.post(self.url, {"appID":self.appointment_unassigned_1.id})
        self.appointment_unassigned_1.refresh_from_db()
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.appointment_unassigned_1.invoice_generated)

    def test_unflag_invoice(self):
        self.client.cookies["authToken"] = self.valid_token

        self.assertTrue(self.appointment_assigned.invoice_generated)

        response = self.client.post(self.url, {"appID":self.appointment_assigned.id})
        self.appointment_assigned.refresh_from_db()
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.appointment_assigned.invoice_generated)