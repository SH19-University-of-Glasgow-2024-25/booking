from rest_framework.exceptions import AuthenticationFailed
from rest_framework.test import APIRequestFactory
from unittest import TestCase
from rest_framework.response import Response
from bookingandbilling.utilities import custom_exception_handler

class TestCustomExceptionHandler(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_authentication_failed(self):
        request = self.factory.get("/")

        # This is the code that is used in the custom authenticator
        response = Response({"detail": "invalid-token"}, status=401)
        response.headers["Set-Cookie"] = "authToken=; Max-Age=0"  # Mocking cookie deletion
        request._auth_failed_response = response
        exception = AuthenticationFailed("Invalid token")
        context = {"request": request}

        response = custom_exception_handler(exception, context)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Set-Cookie", response.headers)
        self.assertIn("authToken=;", response.headers["Set-Cookie"])
        self.assertIn("Max-Age=0", response.headers["Set-Cookie"])
