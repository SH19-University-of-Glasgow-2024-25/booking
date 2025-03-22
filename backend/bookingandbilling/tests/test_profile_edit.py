from django.urls import reverse
from rest_framework.test import APIClient
from django.test import TestCase

from rest_framework.authtoken.models import Token
from bookingandbilling.models import Admin, Customer, Gender, Interpreter
from bookingandbilling.serializers.edit_user_serializers import (AdminEditAdminSerializer, 
                                                                 AdminEditCustomerSerializer, 
                                                                 AdminEditInterpreterSerializer, 
                                                                 SelfEditAdminSerializer, 
                                                                 SelfEditCustomerSerializer, 
                                                                 SelfEditInterpreterSerializer)

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.editing_admin = Admin.objects.create(email="editing_admin@example.com")
        self.other_admin = Admin.objects.create(email="other_admin@example.com")

        self.interpreter = Interpreter.objects.create(email="interpreter@example.com", 
                                                      first_name="Interp", last_name="Reter", 
                                                      address="an address", postcode="G20 8PN", 
                                                      gender=Gender.MALE)

        self.customer = Customer.objects.create(email="customer@example.com", first_name="Custé", 
                                                last_name="O'mer", 
                                                organisation="Government of Glasgow")

        self.editing_admin_token, _created = Token.objects.get_or_create(user=self.editing_admin)
        self.other_admin_token, _created = Token.objects.get_or_create(user=self.other_admin)
        self.interpreter_token, _created = Token.objects.get_or_create(user=self.interpreter)
        self.customer_token, _created = Token.objects.get_or_create(user=self.customer)

class TestGetFields(BaseTestCase):
    def setUp(self):
        super().setUp()
    
    def test_admin_get_fields_of_admin(self):
        self.client.cookies["authToken"] = self.editing_admin_token

        url = reverse("get_user_edit_fields") + f"?user={self.other_admin.email}"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["result"]["user-type"], "admin")
        
        for field in AdminEditAdminSerializer.Meta.fields:
            self.assertIn(field, response.data["result"]["fields"])
    
    def test_admin_get_fields_of_interpreter(self):
        self.client.cookies["authToken"] = self.editing_admin_token

        url = reverse("get_user_edit_fields") + f"?user={self.interpreter.email}"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["result"]["user-type"], "interpreter")
        
        for field in AdminEditInterpreterSerializer.Meta.fields:
            self.assertIn(field, response.data["result"]["fields"])
    
    def test_admin_get_fields_of_customer(self):
        self.client.cookies["authToken"] = self.editing_admin_token

        url = reverse("get_user_edit_fields") + f"?user={self.customer.email}"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["result"]["user-type"], "customer")
        
        for field in AdminEditCustomerSerializer.Meta.fields:
            self.assertIn(field, response.data["result"]["fields"])
    
    def test_non_admin_get_fields_of_other(self): # Should fail
        self.client.cookies["authToken"] = self.customer_token

        url = reverse("get_user_edit_fields") + f"?user={self.interpreter.email}"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 403)
    
    def test_admin_get_fields_of_self(self):
        self.client.cookies["authToken"] = self.other_admin_token

        url = reverse("get_user_edit_fields") + "?user=self"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["result"]["user-type"], "admin")
        
        for field in SelfEditAdminSerializer.Meta.fields:
            self.assertIn(field, response.data["result"]["fields"])
    
    def test_interpreter_get_fields_of_self(self):
        self.client.cookies["authToken"] = self.interpreter_token

        url = reverse("get_user_edit_fields") + "?user=self"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["result"]["user-type"], "interpreter")
        
        for field in SelfEditInterpreterSerializer.Meta.fields:
            self.assertIn(field, response.data["result"]["fields"])

    def test_customer_get_fields_of_self(self):
        self.client.cookies["authToken"] = self.customer_token

        url = reverse("get_user_edit_fields") + "?user=self"
        response = self.client.get(url)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.data["result"]["user-type"], "customer")
        
        for field in SelfEditCustomerSerializer.Meta.fields:
            self.assertIn(field, response.data["result"]["fields"])

class TestEditUser(BaseTestCase):
    def setUp(self):
        super().setUp()
    
    def test_admin_edit_admin_valid(self):
        self.client.cookies["authToken"] = self.editing_admin_token
        user = self.other_admin

        url = reverse("edit_profile") + f"?user={user.email}"

        data = {
            "password": "new_password",
            "first_name": "Adam",
            "last_name": "Inn",
            "email": "updated_admin@example.com",
            "phone_number": "0",
            "alt_phone_number": "0",
            "notes": "Some notes..."
        }

        response = self.client.post(
            url, data, format="multipart")
        
        print(response.data)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_edit_admin_invalid(self):
        self.client.cookies["authToken"] = self.editing_admin_token
        user = self.other_admin

        url = reverse("edit_profile") + f"?user={user.email}"

        data = {
            "password": "new_password",
            "first_name": "",
            "last_name": "",
            "email": "updated_admin@example.com",
            "phone_number": "0",
            "alt_phone_number": "0",
            "notes": "Some notes..."
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
    
    def test_admin_edit_customer_valid(self):
        self.client.cookies["authToken"] = self.editing_admin_token
        user = self.customer

        url = reverse("edit_profile") + f"?user={user.email}"

        data = {
            "password": "new_password",
            "first_name": "Custard",
            "last_name": "Omer",
            "email": "updated_customer@example.com",
            "organisation": "Glasgow World Government",
            "phone_number": "0",
            "alt_phone_number": "0",
            "postcode": "G12 8RZ",
            "address": "1 Glasgow Street",
            "notes": "Some notes..."
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_edit_customer_invalid(self):
        self.client.cookies["authToken"] = self.editing_admin_token
        user = self.customer

        url = reverse("edit_profile") + f"?user={user.email}"

        data = {
            "password": "",
            "first_name": "Custard",
            "last_name": "Omer",
            "email": "updated_customer@example.com",
            "organisation": "Glasgow World Government",
            "phone_number": "0",
            "alt_phone_number": "0",
            "postcode": "G12 8RZ",
            "address": "1 Glasgow Street",
            "notes": "Some notes..."
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertNotEqual(response.status_code, 200)
    
    def test_admin_edit_interpreter_valid(self):
        self.client.cookies["authToken"] = self.editing_admin_token
        user = self.interpreter

        url = reverse("edit_profile") + f"?user={user.email}"

        data = {
            "password": "new_password",
            "first_name": "Intern",
            "last_name": "Preeta",
            "gender": Gender.MALE,
            "email": "updated_interpreter@example.com",
            "address": "1 Glasgow Street",
            "postcode": "G12 8RZ",
            "phone_number": "0",
            "alt_phone_number": "0",
            "notes": "Some notes..."
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_edit_interpreter_invalid(self):
        self.client.cookies["authToken"] = self.editing_admin_token
        user = self.interpreter

        url = reverse("edit_profile") + f"?user={user.email}"

        data = {
            "password": "new_password",
            "first_name": "Intern",
            "last_name": "Preeta",
            "gender": Gender.MALE,
            "email": "updated_interpreter",
            "address": "1 Glasgow Street",
            "postcode": "G12 8RZ",
            "phone_number": "0",
            "alt_phone_number": "0",
            "notes": "Some notes..."
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
    
    def test_admin_edit_self_valid(self):
        self.client.cookies["authToken"] = self.other_admin_token

        url = reverse("edit_profile") + "?user=self"

        data = {
            "password": "new_password",
            "first_name": "Adam",
            "last_name": "Inn",
            "email": "updated_admin@example.com",
            "phone_number": "0",
            "alt_phone_number": "0"
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_admin_edit_self_invalid(self):
        self.client.cookies["authToken"] = self.other_admin_token

        url = reverse("edit_profile") + "?user=self"

        data = {
            "password": "new_password",
            "first_name": 0,
            "last_name": "Inn",
            "email": "updated_admin",
            "phone_number": "0",
            "alt_phone_number": "0"
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
    
    def test_customer_edit_self_valid(self):
        self.client.cookies["authToken"] = self.customer_token

        url = reverse("edit_profile") + "?user=self"

        data = {
            "password": "new_password",
            "first_name": "Custard",
            "last_name": "Omer",
            "email": "updated_customer@example.com",
            "organisation": "Glasgow World Government",
            "postcode": "G12 8RZ",
            "address": "1 Glasgow Street",
            "phone_number": "0",
            "alt_phone_number": "0"
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_customer_edit_self_invalid(self):
        self.client.cookies["authToken"] = self.customer_token

        url = reverse("edit_profile") + "?user=self"

        data = {
            "password": "new_password",
            "first_name": "Custard",
            "organisation": "Glasgow World Government",
            "postcode": "G12 8RZ",
            "address": "1 Glasgow Street",
            "phone_number": "0",
            "alt_phone_number": "0"
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
    
    def test_interpreter_edit_self_valid(self):
        self.client.cookies["authToken"] = self.interpreter_token

        url = reverse("edit_profile") + "?user=self"

        data = {
            "password": "new_password",
            "first_name": "Intern",
            "last_name": "Preeta",
            "email": "updated_interpreter@example.com",
            "gender": Gender.MALE,
            "address": "1 Glasgow Street",
            "postcode": "G12 8RZ",
            "phone_number": "0",
            "alt_phone_number": "0",
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
    
    def test_interpreter_edit_self_invalid(self):
        self.client.cookies["authToken"] = self.interpreter_token

        url = reverse("edit_profile") + "?user=self"

        data = {
            "password": "new_password",
            "first_name": "Intern",
            "last_name": "Preeta",
            "email": "updated_interpreter",
            "address": "1 Glasgow Street",
            "postcode": "G12 8RZ",
            "phone_number": "0",
            "alt_phone_number": "0",
        }

        response = self.client.post(
            url, data, format="multipart")
        
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)
