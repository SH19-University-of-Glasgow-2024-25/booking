from django.test import TestCase, RequestFactory
from rest_framework.exceptions import AuthenticationFailed
from bookingandbilling.views.views_utility import IsUserType
from bookingandbilling.middleware import CookieTokenAuthentication
from bookingandbilling.models import (
    AccountType,
    Admin,
    Interpreter,
    Customer,
)
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APIClient


class CookieTokenAuthenticationTestCase(TestCase):
    """
    
    Test custom cookie token authenticator

    setUp: create required variables
    mock_authenticate_credentials: mock authenticate method allowing us to test only the custom code
    test_authenticate_with_valid_token: simulate authenticator call with valid token
    test_authenticate_with_invalid_token: simulate authenticator call with invalid token
    test_authenticate_without_token: simulate authenticator call without token
    
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.auth = CookieTokenAuthentication()
        self.valid_token = "valid_token"
        self.invalid_token = "invalid_token"

    def mock_authenticate_credentials(self, token):
        if token == self.valid_token:
            return ("user_object", None)  # Simulate a valid user object and authentication details
        else:
            raise AuthenticationFailed("Invalid token")

    def test_authenticate_with_valid_token(self):
        request = self.factory.get("/")
        request.COOKIES["authToken"] = self.valid_token

        self.auth.authenticate_credentials = self.mock_authenticate_credentials

        user, auth = self.auth.authenticate(request)
        self.assertEqual(user, "user_object")
        self.assertIsNone(auth)

    def test_authenticate_with_invalid_token(self):
        request = self.factory.get("/")
        request.COOKIES["authToken"] = self.invalid_token

        self.auth.authenticate_credentials = self.mock_authenticate_credentials

        with self.assertRaises(AuthenticationFailed):
            self.auth.authenticate(request)

    def test_authenticate_without_token(self):
        request = self.factory.get("/")

        result = self.auth.authenticate(request)
        self.assertIsNone(result)


class LoginTestCase(TestCase):
    """
    
    Test login functionality / endpoint

    setUp: create required variables
    test_login_all_accounts: simulate login with an admin, interpreter, and approved customer
    test_login_not_approved_customers: simulate login with unapproved customer
    test_login_with_invalid_credentials: simulate logins with invalid credentials
    
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = Admin.objects.create(
            first_name="John",
            last_name="Brown",
            email="johnbrown@gmail.com",
        )
        self.interpreter = Interpreter.objects.create(
            first_name="Freddy",
            last_name="Johnson",
            email="multilingualinterpreter@gmail.com",
        )
        self.customer = Customer.objects.create(
            first_name="Bartholomew",
            last_name="Richard",
            email="barthrich4000@plusnet.com",
            approved=True,
            email_validated=True,
        )
        self.admin.set_password("password")
        self.admin.save()
        self.interpreter.set_password("password")
        self.interpreter.save()
        self.customer.set_password("password")
        self.customer.save()
        self.url = "/api/login/"

    def test_login_all_accounts(self):
        for account, type in [
            (self.admin, AccountType.ADMIN),
            (self.interpreter, AccountType.INTERPRETER),
            (self.customer, AccountType.CUSTOMER)
        ]:
            response = self.client.post(
                self.url,
                {
                    "email" : account.email,
                    "password" : "password",
                },
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["result"]["account_type"], type)
            self.assertIn("authToken", response.cookies)

            try:
                Token.objects.get(key=response.data["result"]["token"])
            except Token.DoesNotExist:
                self.fail("Token does not exist")

    def test_login_not_approved_customer(self):
        self.customer.approved = False
        self.customer.save()

        response = self.client.post(
            self.url,
            {
                "email" : self.customer.email,
                "password" : "password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_with_invalid_credentials(self):
        for email, password in [
            (self.admin.email, "wrongPassword"),
            ("wrong@email.com", "password")
        ]:
            response = self.client.post(
                self.url,
                {
                    "email" : email,
                    "password" : password,
                },
                format="json",
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LogoutTestCase(TestCase):
    """
    
    Test logout functionality / endpoint

    setUp: create required variables
    test_logout_with_valid_token: simulate logout with a valid token
    test_logout_with_invalid_token: simulate logout with an invalid token
    test_logout_without_token: simulate logout without a token
    
    """

    def setUp(self):
        self.client = APIClient()
        self.admin = Admin.objects.create(
            first_name="John",
            last_name="Brown",
            email="johnbrown@gmail.com"
        )
        self.token, _created = Token.objects.get_or_create(user=self.admin)
        self.url = "/api/logout/"

    def test_logout_with_valid_token(self):
        self.client.cookies["authToken"] = self.token.key
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"]["message"], "Logged out successfully")

        # Assert the token is deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(key=self.token.key)

        self.assertEqual(response.cookies["authToken"].value, "")

    def test_logout_with_invalid_token(self):
        self.client.cookies["authToken"] = "invalid_token"
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_without_token(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AccountTypePermissionTestCase(TestCase):
    """
    
    Test custom account type endpoint permission

    setUp: create required variables
    test_valid_permission: simulate permission check with valid token
    test_invalid_permission: simulate permission check with invalid token
    test_all_valid_permission: simulate permission check with valid token on full access
    
    """

    def setUp(self):
        self.factory = RequestFactory()
        self.admin = Admin.objects.create(
            first_name="John",
            last_name="Brown",
            email="johnbrown@gmail.com"
        )
        self.interpreter = Interpreter.objects.create(
            first_name="Sarah",
            last_name="Pickford",
            email="notapproved@gmail.com"
        )
        self.customer = Customer.objects.create(
            first_name="Yogi",
            last_name="Bear",
            email="picnicbaskets@jellystone.com"
        )
        self.permission = IsUserType(allowed_types=[AccountType.ADMIN])

    def test_valid_permission(self):
        request = self.factory.get("/")
        token, _created = Token.objects.get_or_create(user=self.admin)
        request.COOKIES["authToken"] = token

        self.assertTrue(self.permission.has_permission(request, None))

    def test_invalid_permission(self):
        request = self.factory.get("/")
        token, _created = Token.objects.get_or_create(user=self.interpreter)
        request.COOKIES["authToken"] = token

        self.assertFalse(self.permission.has_permission(request, None))

    def test_all_valid_permission(self):
        permission = IsUserType(
            allowed_types=[
                AccountType.ADMIN,
                AccountType.INTERPRETER,
                AccountType.CUSTOMER,
            ]
        )

        for account in [self.admin, self.interpreter, self.customer]:
            request = self.factory.get("/")
            token, _created = Token.objects.get_or_create(user=account)
            request.COOKIES["authToken"] = token

            self.assertTrue(permission.has_permission(request, None))