from django.contrib.auth import authenticate
from ..models import AccountType
from .views_utility import get_full_user, get_user_from_token

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from ..serializers.authentication_serializers import (
    LoginSerializer, 
    UserSerializer
)
from ..utilities import (
    APIresponse,
    APIerror,
    ErrorResponse
)

class CheckAuthView(APIView):
    def get(self, request):
        token = request.COOKIES.get('authToken')
        user = get_user_from_token(token)
        user, user_type = get_full_user(user)
        return APIresponse(
                {
                    "message": "Authenticated!",
                    "account_type": user_type,
                }
                          )

        
class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('authToken')
        Token.objects.get(key=token).delete()
        response = APIresponse({"message": "Logged out successfully"})
        response.delete_cookie('authToken')
        return response
    
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(username=email, password=password)
            user, user_type = get_full_user(user)

            # user found
            if user is not None:
                if user_type == AccountType.CUSTOMER: 
                    if user.approved:
                        # can log in
                        pass
                    elif user.email_validated:
                        # has not been approved yet
                        return ErrorResponse(
                                APIerror(
                                    "account-unapproved",
                                    status.HTTP_403_FORBIDDEN,
                                    "Account yet to be approved by admins."
                                )
                                            )

                    else:
                        # has not verified email
                        return ErrorResponse(
                                APIerror(
                                    "account-unverified",
                                    status.HTTP_403_FORBIDDEN,
                                    "Email yet to be verified - Check your inbox."
                                )
                                            )

                token, _created = Token.objects.get_or_create(user=user)
                user_serializer = UserSerializer(user)

                response = APIresponse({
                        "token": token.key,
                        "user": user_serializer.data,
                        "account_type": user_type,
                                       })

                response.set_cookie(
                    'authToken',
                    token.key,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    max_age=86400,  # 1 day in seconds
                )
                
                return response
            
            # user not found
            else:
                return ErrorResponse(
                        APIerror(
                            "invalid-credentials",
                            status.HTTP_403_FORBIDDEN,
                            "Invalid credentials provided"
                        )
                                    )

        return ErrorResponse(
                APIerror("input-errors", 
                         status.HTTP_400_BAD_REQUEST, 
                         "Errors in login inputs.", 
                         error_list=serializer.errors))
