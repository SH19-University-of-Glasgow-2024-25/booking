from django.test import TestCase
from rest_framework.test import APIClient
from bookingandbilling.serializers.registration_serializers import (
    RegisterAdminSerializer,
    RegisterCustomerSerializer,
    RegisterInterpreterSerializer,
)
from bookingandbilling.models import (
    Admin,
    Interpreter,
    Customer,
    Gender,
    Tag,
    Language,
)
from rest_framework.authtoken.models import Token
from rest_framework import status
from unittest.mock import patch


class RegisterAdminSerializerTestCase(TestCase):
    """
    
    Test admin registration serializer

    test_valid_data: test serializer with valid data
    test_optional_data: test serializer is valid without optional fields
    test_required_data: test serializer is invalid without any required fields
    test_invalid_data: test serializer is invalid with invalid password or email
    
    """

    def setUp(self):
        self.data = {
            "first_name": "lightning",
            "last_name": "mcqueen",
            "email": "speed@racing.com",
            "password": "strongPassword12",
            "confirm_password": "strongPassword12",
            "phone_number": "01234567890",
            "alt_phone_number": "09876543210",
            "notes": "This account is a test!",
        }

    def test_valid_data(self):
        serializer = RegisterAdminSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        admin = serializer.save()
        self.assertEqual(admin.__class__, Admin)

    def test_optional_data(self):
        self.data.pop("phone_number")
        self.data.pop("alt_phone_number")
        self.data.pop("notes")

        serializer = RegisterAdminSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_required_fields(self):
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
        ]

        for required_field in required_fields:
            temp = self.data.pop(required_field)
            serializer = RegisterAdminSerializer(data=self.data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(required_field, serializer.errors)
            self.data[required_field] = temp

    def test_invalid_data(self):
        self.data["email"] = "invalid.email"
        serializer = RegisterAdminSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.data["email"] = "valid@email.com"

        self.data["confirm_password"] = "differentPassword"
        serializer = RegisterAdminSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class RegisterInterpreterSerializerTestCase(TestCase):
    """
    
    Test interpreter registration serializer

    test_valid_data: test serializer with valid data
    test_optional_data: test serializer is valid without optional fields
    test_required_data: test serializer is invalid without any required fields
    test_invalid_data: test serializer is invalid with invalid password or email
    
    """

    def setUp(self):
        self.on_holiday = Tag.objects.create(
            name="On Holiday",
            colour="#ffff00"
        )
        self.multilingual = Tag.objects.create(
            name="Multilingual",
            colour="#0082EF"
        )
        self.english = Language.objects.create(language_name="English")
        self.spanish = Language.objects.create(language_name="Spanish")
        self.data = {
            "first_name": "lightning",
            "last_name": "mcqueen",
            "email": "speed@racing.com",
            "password": "strongPassword12",
            "confirm_password": "strongPassword12",
            "phone_number": "01234567890",
            "alt_phone_number": "09876543210",
            "notes": "This account is a test!",
            "address": "12 Fake Street",
            "postcode": "G34 P92",
            "gender": Gender.MALE,
            "languages": [
                self.english.language_name,
                self.spanish.language_name,
            ],
            "tag": [
                self.on_holiday.name,
                self.multilingual.name,
            ],
        }

    def test_valid_data(self):
        serializer = RegisterInterpreterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        interpreter = serializer.save()
        self.assertEqual(interpreter.__class__, Interpreter)
        self.assertIn(self.english, interpreter.languages.all())
        self.assertIn(self.spanish, interpreter.languages.all())
        self.assertIn(self.on_holiday, interpreter.tag.all())
        self.assertIn(self.multilingual, interpreter.tag.all())

    def test_optional_data(self):
        self.data.pop("phone_number")
        self.data.pop("alt_phone_number")
        self.data.pop("notes")
        self.data.pop("languages")
        self.data.pop("tag")

        serializer = RegisterInterpreterSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_required_fields(self):
        required_fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "address",
            "postcode",
            "gender",
        ]

        for required_field in required_fields:
            temp = self.data.pop(required_field)
            serializer = RegisterInterpreterSerializer(data=self.data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(required_field, serializer.errors)
            self.data[required_field] = temp

    def test_invalid_data(self):
        self.data["email"] = "invalid.email"
        serializer = RegisterInterpreterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.data["email"] = "valid@email.com"

        self.data["confirm_password"] = "differentPassword"
        serializer = RegisterInterpreterSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class RegisterCustomerSerializerTestCase(TestCase):
    """
    
    Test customer registration serializer

    test_valid_data: test serializer with valid data
    test_optional_data: test serializer is valid without optional fields
    test_required_data: test serializer is invalid without any required fields
    test_invalid_data: test serializer is invalid with invalid password or email
    
    """

    def setUp(self):
        self.data = {
            "first_name": "lightning",
            "last_name": "mcqueen",
            "organisation": "Pixar",
            "email": "speed@racing.com",
            "password": "strongPassword12",
            "confirm_password": "strongPassword12",
            "phone_number": "01234567890",
            "alt_phone_number": "09876543210",
            "notes": "This account is a test!",
            "address": "12 Fake Street",
            "postcode": "G34 P92",
        }

    def test_valid_data(self):
        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

        customer = serializer.save()
        self.assertEqual(customer.__class__, Customer)

    def test_optional_data(self):
        self.data.pop("phone_number")
        self.data.pop("alt_phone_number")
        self.data.pop("notes")

        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_required_fields(self):
        required_fields = [
            "first_name",
            "last_name",
            "organisation",
            "email",
            "password",
            "confirm_password",
            "address",
            "postcode",
        ]

        for required_field in required_fields:
            temp = self.data.pop(required_field)
            serializer = RegisterCustomerSerializer(data=self.data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(required_field, serializer.errors)
            self.data[required_field] = temp

    def test_invalid_data(self):
        self.data["email"] = "invalid.email"
        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.data["email"] = "valid@email.com"

        self.data["confirm_password"] = "differentPassword"
        serializer = RegisterCustomerSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)


class AdminProtectedRegistrationViewTestCase(TestCase):
    """
    
    Test admin protected registration end point

    test_invalid_tokens: test endpoint calls with invalid tokens
    test_admin_creation: test endpoint to create admin
    test_customer_creation: test endpoint to create customer
    test_interpreter_creation: test endpoint to create interpreter
    
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = Admin.objects.create(email="johnbrown@gmail.com")
        self.interpreter = Interpreter.objects.create(email="multilingualinterpreter@gmail.com")
        self.valid_token, _created = Token.objects.get_or_create(user=self.admin)
        self.invalid_token, _created = Token.objects.get_or_create(user=self.interpreter)
        self.url = "/api/register-admin/"

        self.account_data = {
            "first_name": "lightning",
            "last_name": "mcqueen",
            "email": "speed@racing.com",
            "password": "strongPassword12",
            "confirm_password": "strongPassword12",
            "phone_number": "01234567890",
            "alt_phone_number": "09876543210",
            "notes": "This account is a test!",
        }

    def test_invalid_tokens(self):
        # no token
        response = self.client.post(self.url, self.account_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # not admin token
        self.client.cookies["authToken"] = self.invalid_token
        response = self.client.post(self.url, self.account_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_creation(self):
        self.client.cookies["authToken"] = self.valid_token
        self.account_data["type"] = "admin"

        response = self.client.post(self.url, self.account_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Admin.objects.filter(email=self.account_data["email"]).exists())

    def test_customer_creation(self):
        self.client.cookies["authToken"] = self.valid_token
        self.account_data["type"] = "customer"
        self.account_data["address"] = "12 Fake Street"
        self.account_data["postcode"] = "G34 P08"
        self.account_data["organisation"] = "Pixar"

        response = self.client.post(self.url, self.account_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Customer.objects.filter(
                email=self.account_data["email"],
                approved=True,
                email_validated=True,
            ).exists()
        )

    def test_interpreter_creation(self):
        self.client.cookies["authToken"] = self.valid_token
        self.account_data["type"] = "interpreter"
        self.account_data["address"] = "12 Fake Street"
        self.account_data["postcode"] = "G34 P08"
        self.account_data["gender"] = Gender.PREFER_NOT_TO_SAY

        on_holiday = Tag.objects.create(
            name="On Holiday",
            colour="#ffff00"
        )
        multilingual = Tag.objects.create(
            name="Multilingual",
            colour="#0082EF"
        )
        english = Language.objects.create(language_name="English")
        spanish = Language.objects.create(language_name="Spanish")
        self.account_data["tag"] = [
            on_holiday.name,
            multilingual.name,
        ]
        self.account_data["languages"] = [
            english.language_name,
            spanish.language_name,
        ]

        response = self.client.post(self.url, self.account_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Interpreter.objects.filter(email=self.account_data["email"]).exists())


class CustomerRegistrationRequestViewTestCase(TestCase):
    """
    
    Test customer request registration end point

    test_customer_creation: test endpoint for unapproved and invalidated customer
    
    """

    @patch("bookingandbilling.views.views_registration.send_validation_email")
    def test_customer_creation(self, mock_send_validation_email):
        mock_send_validation_email.return_value = None

        account_data = {
            "first_name": "lightning",
            "last_name": "mcqueen",
            "organisation": "Pixar",
            "email": "speed@racing.com",
            "password": "strongPassword12",
            "confirm_password": "strongPassword12",
            "phone_number": "01234567890",
            "alt_phone_number": "09876543210",
            "notes": "This account is a test!",
            "address": "12 Fake Street",
            "postcode": "G43 U76",
        }

        response = self.client.post("/api/register-customer/", account_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Customer.objects.filter(email=account_data["email"]).exists())