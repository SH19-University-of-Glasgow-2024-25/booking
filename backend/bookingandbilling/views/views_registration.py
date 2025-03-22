import traceback

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from ..models import AccountType, Customer, User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.http import HttpResponse
from django.shortcuts import redirect
from .views_utility import get_full_user, get_user_from_token, IsUserType

from ..tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from ..email_utils import send_reset_email, send_validation_email

from ..serializers.registration_serializers import (
    RegisterAdminSerializer,
    RegisterCustomerSerializer,
    RegisterInterpreterSerializer,
)
from ..utilities import (
    APIresponse,
    APIerror,
    ErrorResponse,
    INTERNAL_ERROR_RESPONSE
)


class AccountAcceptanceView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email") # email for user
            accepted = request.data.get("accepted") # boolean for accepted or not

            if email is None:
                return ErrorResponse(
                        APIerror(
                            "no-email",
                            status.HTTP_400_BAD_REQUEST,
                            "An email is required."
                        )
                                    )
            if accepted is None:
                return ErrorResponse(
                        APIerror(
                            "no-acceptance",
                            status.HTTP_400_BAD_REQUEST,
                            "Acceptance is required."
                        )
                                    )
            
            user = User.objects.get(email=email)

            if hasattr(user, 'customer'):
                user = user.customer
            else:
                return ErrorResponse(
                        APIerror(
                            "incompatible-user-type",
                            status.HTTP_400_BAD_REQUEST,
                            "User is not a customer."
                        )
                                    )
            
            if accepted:
                # send acceptance email?
                user.approved = True
                user.save()
            else:
                # send decline email?
                user.delete()
            
            return APIresponse({"message": "Account acceptance processed successfully."})
        
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE

            
class AccountRequestFeedView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def get(self, request, *args, **kwargs):
        try:
            customers = Customer.objects.filter(
                email_validated=True,
                approved=False
            ).order_by('date_joined')
            
            response_data = {
                "customers": [
                    {
                        "first_name": customer.first_name,
                        "last_name": customer.last_name,
                        "organisation": customer.organisation,
                        "email": customer.email,
                        "phone_number": customer.phone_number,
                        "address": customer.address,
                        "postcode": customer.postcode,
                    }
                    for customer in customers
                ],
            }
            
            return APIresponse(response_data)
        
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE
            

class RegisterAdminViewSet(CreateAPIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def get_serializer_class(self):
        user_type = self.request.data.get("type")
        if user_type == "admin":
            return RegisterAdminSerializer
        elif user_type == "interpreter":
            return RegisterInterpreterSerializer
        elif user_type == "customer":
            return RegisterCustomerSerializer
        raise ValidationError({"type": "Invalid type specified."})

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()

                # If creating customer, set approval to true as being made by admin
                if serializer_class == RegisterCustomerSerializer:
                    user.approved = True
                    user.email_validated = True
                    token = request.COOKIES.get('authToken')
        
                    admin = get_user_from_token(token)
                    admin, user_type = get_full_user(admin)
                    user.approver = admin
                    
                    user.save()
                    
            except (ValidationError, IntegrityError, ValueError) as e:
                print(traceback.print_exception(e))
                return ErrorResponse(
                        APIerror(
                            "django-error", 
                            status.HTTP_400_BAD_REQUEST, 
                            "Django model unable to be created"
                               )
                               )
            except Exception as e:
                print(traceback.print_exception(e))
                return INTERNAL_ERROR_RESPONSE

            token, _created = Token.objects.get_or_create(user=user)
    
            return APIresponse(
                {
                    "user": serializer.data,
                    "token": token.key
                },
                status.HTTP_201_CREATED
            )
        
        return ErrorResponse(
                APIerror("input-errors", 
                         status.HTTP_400_BAD_REQUEST, 
                         "Errors in registration user inputs.", 
                         error_list=serializer.errors))
    
class RegisterCustomerViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterCustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save()
            except (ValidationError, IntegrityError, ValueError) as e:
                print(traceback.print_exception(e))
                return ErrorResponse(
                        APIerror(
                            "django-error", 
                            status.HTTP_400_BAD_REQUEST, 
                            "Django model unable to be created"
                               )
                               )
            except Exception as e:
                print(traceback.print_exception(e))
                return INTERNAL_ERROR_RESPONSE
            
            try:
                send_validation_email(request, user)
            except Exception as e:
                user.delete()
                print(traceback.print_exception(e))
                return ErrorResponse(
                        APIerror(
                            "email-send-failure", 
                            status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            "Verification email failed to send."
                               )
                               )

            token, _created = Token.objects.get_or_create(user=user)
    
            return APIresponse({"user": serializer.data, 
                                "token": token.key},
                               status.HTTP_201_CREATED)
        
        return ErrorResponse(
                APIerror("input-errors", 
                         status.HTTP_400_BAD_REQUEST, 
                         "Errors in registration user inputs.", 
                         error_list=serializer.errors))

def check_email_validation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
        user = user.customer

        if account_activation_token.check_token(user, token):
            user.email_validated = True
            user.save()
            return HttpResponse(
                "Thank you for verifying your email! \
                Admins will now review your account request."
            )
        else:
            return HttpResponse( 
                "Oops. Something went wrong!"
            )

    except Exception as e:
        print(traceback.print_exception(e))
        return HttpResponse(
            "Oops. Something went wrong!"
        )
    
    
class SendPasswordResetEmail(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return ErrorResponse(
                APIerror(
                    "no-email",
                    status.HTTP_400_BAD_REQUEST,
                    "An email is required."
                )
            )
        try:
            user = User.objects.get(email=email)
            send_reset_email(request, user)
            return APIresponse({"message": "Password reset email sent successfully."})
        except User.DoesNotExist:
            return ErrorResponse(
                APIerror(
                    "user-not-found",
                    status.HTTP_404_NOT_FOUND,
                    "User with this email does not exist."
                )
            )
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE

class ResendEmailVerification(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return ErrorResponse(
                APIerror(
                    "no-email",
                    status.HTTP_400_BAD_REQUEST,
                    "An email is required."
                )
            )

        try:
            user = Customer.objects.get(email=email)
        except User.DoesNotExist:
            return ErrorResponse(
                APIerror(
                    "user-not-found",
                    status.HTTP_404_NOT_FOUND,
                    "No user is associated with this email."
                )
            )

        send_validation_email(request, user)
        return APIresponse(
            {
                "message": f"Validation email sent to {email}."
            }
        )

       
def new_password_validation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        token_generator = PasswordResetTokenGenerator()
        user = User.objects.get(email=uid)

        if token_generator.check_token(user, token):
            base_host = request.get_host() 
            frontend_host = base_host.replace(':8000', ':5173')  

            frontend_url = f'http://{frontend_host}/update-password/{uidb64}/{token}/'
            return redirect(frontend_url)
        else:
            return HttpResponse( 
                "Oops. Something went wrong!"
            )

    except Exception as e:
        print(traceback.print_exception(e))
        return HttpResponse(
            "Oops. Something went wrong!"
        )


class UpdatePassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        uid = force_str(urlsafe_base64_decode(request.data.get("uidb64")))
        token = request.data.get("token")
        password = request.data.get("password")
        
        user = User.objects.get(email=uid)
        
        token_generator = PasswordResetTokenGenerator()
        if (token_generator.check_token(user,token)):
            user.set_password(password)
            user.save()
            return APIresponse({"message": "Password updated successfully."})
        else:
            return ErrorResponse(
                APIerror(
                    "invalid-token",
                    status.HTTP_400_BAD_REQUEST,
                    "Invalid token provided."
                )
            )