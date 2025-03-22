from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

# Method of authenticating API requests using HTTP-Only cookies
class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('authToken')
        if not token:
            return None
        
        try:
            return self.authenticate_credentials(token)
        except AuthenticationFailed:
            response = Response({"detail": "invalid-token"}, status=401)
            response.delete_cookie('authToken')
            request._auth_failed_response = response
            raise AuthenticationFailed("Invalid Token")

# Middleware to allow cross-origin for API
class ApiMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Methods"] = "*"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

        return response