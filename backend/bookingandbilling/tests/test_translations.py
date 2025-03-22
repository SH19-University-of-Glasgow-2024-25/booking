import json
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from bookingandbilling.serializers.translation_serializers import (
    CreateTranslationSerializer
)
from bookingandbilling.models import (
    Admin,
    Customer,
    Interpreter,
    Language,
    Translation
)

class BaseTestCase(TestCase):

    def setUp(self):
        self.interpreter_1 = Interpreter.objects.create(
            first_name="Main",
            last_name="Interp",
            email="thisisanemail@gmail.com"
        )
        self.interpreter_2 = Interpreter.objects.create(
            first_name="Side",
            last_name="Interp",
            email="alsoanemail@gmail.com"
        )

        self.translation_1 = Translation.objects.create(
            word_count=100,
            document=SimpleUploadedFile("test_document.txt", b"Document content to be translated")
        )
        self.translation_1.offered_to.add(self.interpreter_1)
        self.translation_1.offered_to.add(self.interpreter_2)
        self.translation_1.save()
        
        self.translation_2 = Translation.objects.create(
            word_count=100,
            document=SimpleUploadedFile("test_document.txt", b"Document content to be translated")
        )
        self.translation_2.offered_to.add(self.interpreter_1)
        self.translation_2.offered_to.add(self.interpreter_2)
        self.translation_2.save()

        self.client = APIClient()
        interpreter_1_token, _created = Token.objects.get_or_create(user=self.interpreter_1)
        self.client.cookies["authToken"] = interpreter_1_token
    

class TranslationSerilaizerTestCase(TestCase):
    """
    
    Test translation creation serializer

    test_valid_data: test serializer with data

    """

    def setUp(self):
        # Create basic admins
        self.admin1 = Admin.objects.create(
            first_name="John",
            last_name="Brown",
            email="johnbrown@gmail.com"
        )

        # Create languages
        self.english = Language.objects.create(language_name="English")
        self.spanish = Language.objects.create(language_name="Spanish")
        self.french = Language.objects.create(language_name="French")
        self.german = Language.objects.create(language_name="German")

        # Create basic customers
        self.customer1 = Customer.objects.create(
            first_name="Bartholomew",
            last_name="Richard",
            email="barthrich4000@plusnet.com",
            address="123 Real Street",
            postcode="ABCD EFG",
            password="password",
            approved=True,
            approver=self.admin1
        )
        self.data = {
            "customer": self.customer1,
            "language":"french",
            "document": SimpleUploadedFile(
                "test_document.pdf", b"Fake content", content_type="application/pdf"
            ),
            "word_count": 120,
            "notes":"notey note note"
        }

    def test_valid_data(self):
        serializer = CreateTranslationSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        translation = serializer.save()
        self.assertEqual(translation.__class__, Translation)
    
    def test_valid_data_without_optional_data(self):
        self.data.pop("notes")
        serializer = CreateTranslationSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        translation = serializer.save()
        self.assertEqual(translation.__class__, Translation)
    
    def test_required_fields(self):
        required_fields = [
            "customer",
            "language",
            "document",
            "word_count"
        ]

        for required_field in required_fields:
            temp = self.data.pop(required_field)
            serializer = CreateTranslationSerializer(data=self.data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(required_field, serializer.errors)
            self.data[required_field] = temp
    
    def test_invalid_data(self):
        self.data["customer"] = "not a customer"
        serializer = CreateTranslationSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("customer", serializer.errors)
        self.data["customer"] = self.customer1

class InterpreterTranslationOfferingsTestCase(BaseTestCase):
    """
    
    Test translation offering and acceptance for interpreters

    test_fetching_offered_translations: test end point for fetching translations offered to user
    test_accepting_translation: test accepting a translation links to user and clears offering list
    test_declining_translation: test declining a translation removes user from offered list

    """

    def test_fetching_offered_translations(self):
        response = self.client.post("/api/offered-translations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["result"]), 2)
    
    def test_accepting_translation(self):
        request_data = {
            "translationID": self.translation_1.id,
            "accepted": True
        }
        response = self.client.post(
            "/api/update-translation/",
            json.dumps(request_data),
            content_type="application/json"
        )
        self.translation_1.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.translation_1.offered_to.count(), 0)
        self.assertEqual(self.translation_1.interpreter, self.interpreter_1)
    
    def test_declining_translation(self):
        request_data = {
            "translationID": self.translation_1.id,
            "accepted": False
        }
        response = self.client.post(
            "/api/update-translation/",
            json.dumps(request_data),
            content_type="application/json"
        )
        self.translation_1.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.translation_1.offered_to.count(), 1)
        self.assertNotIn(
            self.interpreter_1.id,
            self.translation_1.offered_to.values_list("id", flat=True)
        )

class InterpreterAcceptedTranslationOverviewTestCase(BaseTestCase):
    """
    
    Test fetching translation accepted by interpreter

    test_fetching_offered_translations: test fetching interpreter's accepted translations
    test_set_actual_word_count: test setting translation's actual word count
    test_clear_actual_word_count: test clearing translation's actual word count
    test_set_actual_word_count_fake_id: test setting the actual word count of a fake translation

    """

    def test_fetching_accepted_translations(self):
        response = self.client.post("/api/fetch-accepted-translations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["result"]), 0)

        for idx, translation in enumerate([None, self.translation_1, self.translation_2]):
            if translation:
                translation.interpreter = self.interpreter_1
                translation.save()
            response = self.client.post("/api/fetch-accepted-translations/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data["result"]), idx)

    def test_set_actual_word_count(self):
        response = self.client.post(
            "/api/set-translations-actual-word-count/",
            json.dumps({"actualWordCount": 100, "translationID": self.translation_1.id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.translation_1.refresh_from_db()
        self.assertEqual(self.translation_1.actual_word_count, 100)

    def test_clear_actual_word_count(self):
        response = self.client.post(
            "/api/set-translations-actual-word-count/",
            json.dumps({"actualWordCount": None, "translationID": self.translation_1.id}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.translation_1.refresh_from_db()
        self.assertIsNone(self.translation_1.actual_word_count)

    def test_set_actual_word_count_fake_id(self):
        response = self.client.post(
            "/api/set-translations-actual-word-count/",
            json.dumps({"actualWordCount": 100, "translationID": 999}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)