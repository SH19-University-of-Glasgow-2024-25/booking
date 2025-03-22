from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from bookingandbilling.models import Admin, Translation, Customer, Interpreter, Language
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

        self.translation_assigned = Translation.objects.create(
            customer=self.customer,
            language=self.spanish,
            interpreter=self.interpreter_offered,
            invoice_generated=True,
            word_count=100,
        )

        self.translation_unassigned_1 = Translation.objects.create(
            customer=self.customer,
            language=self.spanish,
            word_count=100,
        )

        self.translation_unassigned_2 = Translation.objects.create(
            customer=self.customer,
            language=self.spanish,
            word_count=100,
        )

        self.valid_token, _created = Token.objects.get_or_create(user=self.admin)
        self.invalid_token, _created = Token.objects.get_or_create(user=self.interpreter_offered)

        self.translation_unassigned_1.offered_to.add(self.interpreter_offered)

class TestFetchTranslations(BaseTestCase):
    """
    
    Test fetching translations from backend

    test_invalid_tokens: test trying to fetch translations without valid auth
    test_fetch_assigned_translations: test fetching assigned translations
    test_fetch_unassigned_translations: test fetching unassigned translations
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/fetch-translations/"

    def test_invalid_tokens(self):
        # no token
        response = self.client.post(self.url, {"unassigned" : True})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.post(self.url, {"unassigned" : True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fetch_assigned_translations(self):
        self.client.cookies["authToken"] = self.valid_token
        response = self.client.post(
            self.url, json.dumps({"unassigned": False}), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        ids = [translation['id'] for translation in response.data["result"]]
        self.assertIn(self.translation_assigned.id, ids)
        self.assertNotIn(self.translation_unassigned_1.id, ids)
        self.assertNotIn(self.translation_unassigned_2.id, ids)

    def test_fetch_unassigned_translations(self):
        self.client.cookies["authToken"] = self.valid_token
        response = self.client.post(
            self.url, json.dumps({"unassigned": True}), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        ids = [translation['id'] for translation in response.data["result"]]
        self.assertIn(self.translation_unassigned_1.id, ids)
        self.assertIn(self.translation_unassigned_2.id, ids)
        self.assertNotIn(self.translation_assigned.id, ids)

class TestOfferTranslation(BaseTestCase):
    """
    
    Test offering translations to interpreters

    test_invalid_tokens: test trying to offer translation to interpreter without valid auth
    test_offering_translation: test offer translation to interpreter
    test_unoffering_translation: test unoffer translation to interpreter
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/offer-translations/"

    def test_invalid_tokens(self):
        # no token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_offering_translation(self):
        self.client.cookies["authToken"] = self.valid_token
        request_data = {
            "translationID":self.translation_unassigned_1.id,
            "interpreterID":self.interpreter_unoffered.id,
            "offer":True
        }

        self.assertFalse(self.translation_unassigned_1.offered_to.filter(
            id=self.interpreter_unoffered.id).exists())

        response = self.client.post(
            self.url, json.dumps(request_data), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.translation_unassigned_1.offered_to.filter(
            id=self.interpreter_unoffered.id).exists())

    def test_unoffering_translation(self):
        self.client.cookies["authToken"] = self.valid_token
        request_data = {
            "translationID":self.translation_unassigned_1.id,
            "interpreterID":self.interpreter_offered.id,
            "offer":False
        }

        self.assertTrue(self.translation_unassigned_1.offered_to.filter(
            id=self.interpreter_offered.id).exists())

        response = self.client.post(
            self.url, json.dumps(request_data), content_type="application/json")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.translation_unassigned_1.offered_to.filter(
            id=self.interpreter_offered.id).exists())

class TestFlaggingInvoiceGenerated(BaseTestCase):
    """
    
    Test flagging invoice generated on translations

    test_invalid_tokens: test trying to offer translation to interpreter without valid auth
    test_flag_invoice: test flagging invoice generated on an translation
    test_unflag_invoice: test unflagging invoice generated on an translation
    
    """

    def setUp(self):
        super().setUp()
        self.url = "/api/toggle-translation-invoice/"

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

        self.assertFalse(self.translation_unassigned_1.invoice_generated)

        response = self.client.post(self.url, {"translationID":self.translation_unassigned_1.id})
        self.translation_unassigned_1.refresh_from_db()
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.translation_unassigned_1.invoice_generated)

    def test_unflag_invoice(self):
        self.client.cookies["authToken"] = self.valid_token

        self.assertTrue(self.translation_assigned.invoice_generated)

        response = self.client.post(self.url, {"translationID":self.translation_assigned.id})
        self.translation_assigned.refresh_from_db()
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.translation_assigned.invoice_generated)