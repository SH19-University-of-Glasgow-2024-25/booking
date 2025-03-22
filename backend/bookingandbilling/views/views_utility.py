import traceback

from ..models import AccountType, Language, Translation

from django.http import FileResponse
from django.conf import settings
import os

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token

from ..utilities import (
    APIresponse,
    APIerror,
    ErrorResponse,
    INTERNAL_ERROR_RESPONSE
)


class IsUserType(BasePermission):
    def __init__(self, allowed_types=[]):
        self.allowed_types = allowed_types
        super().__init__()

    def has_permission(self, request, view):
        token = request.COOKIES.get('authToken')
        user = get_user_from_token(token)
        user, user_type = get_full_user(user)
        return user and user_type in self.allowed_types
    
class RetrieveLanguages(APIView):
    def get(self, request):
        try:
            languages = Language.objects.all().values_list('language_name', flat=True)
            response_data = {
                "languages": list(languages)
            }
            return APIresponse(response_data, status.HTTP_200_OK)
        
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE

            
def get_user_from_token(token_key):
    try:
        token = Token.objects.get(key=token_key)  # Get the token object
        user = token.user  # Access the associated user
        return user
    except Token.DoesNotExist:
        return None
    
def get_full_user(user):
    if not user:
        return None, None
    if hasattr(user, 'admin'):
        return user.admin, AccountType.ADMIN
    elif hasattr(user, 'interpreter'):
        return user.interpreter, AccountType.INTERPRETER
    elif hasattr(user, 'customer'):
        return user.customer, AccountType.CUSTOMER
    return None, None


class protected_media(APIView):
    def get(self, request, path):
        if not path:
            return ErrorResponse(
                APIerror("missing-path", status.HTTP_400_BAD_REQUEST, "Path is required")
            )

        file_path = os.path.join(settings.MEDIA_ROOT, "translation_documents", path)
        
        if not os.path.exists(file_path):
            return ErrorResponse(APIerror("404", status.HTTP_404_NOT_FOUND, "File not found"))
        
        translation = Translation.objects.filter(
            document=os.path.join("translation_documents", path)
        ).first()
        user, user_type = get_full_user(request.user)
        
        if translation is None:
            return ErrorResponse(
                APIerror("404", status.HTTP_404_NOT_FOUND, "Translation not found")
            )
        
        if user_type == AccountType.ADMIN:
            return FileResponse(open(file_path, 'rb'))
        elif user_type == AccountType.INTERPRETER:
            interpreter = user.interpreter
            case_1 = translation in interpreter.translations.all()
            case_2 = translation in interpreter.offered_translations.all()
            if case_1 or case_2:
                return FileResponse(open(file_path, 'rb'))
        elif user_type == AccountType.CUSTOMER:
            if translation in user.customer.translations.all():
                return FileResponse(open(file_path, 'rb'))
            
        return ErrorResponse(
                        APIerror(
                            "acceptance-error", 
                            status.HTTP_403_FORBIDDEN, 
                            "Errors in translation."
                        )
                    )