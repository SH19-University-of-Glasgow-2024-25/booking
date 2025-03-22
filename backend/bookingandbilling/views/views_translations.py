import traceback
from .views_utility import IsUserType, get_full_user, get_user_from_token
from rest_framework.views import APIView
from django.core.files.base import ContentFile
import base64

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..serializers.translation_serializers import (
    CreateTranslationSerializer
)

from ..serializers.model_serializers import (
    GetTranslationSerializer
)

from ..models import AccountType, Interpreter, Translation
from ..utilities import (
    APIerror,
    APIresponse,
    INTERNAL_ERROR_RESPONSE,
    ErrorResponse
)

class UnassignedTranslationsView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def get(self, request, *args, **kwargs):
        translations = Translation.objects.filter(interpreter_isnull=True)

        response_data = {
            "translations": [
                {
                    "pk": translation.pk,
                    "document": translation.document,
                    "customer": " ".join([
                        translation.customer.first_name,
                        translation.customer.last_name
                    ]),
                    "word count": translation.word_count,
                    "language": translation.language
                }
                for translation in translations
            ],
        }

        return APIresponse(response_data)

class FetchTranslationsView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request, *args, **kwargs):
        if request.data.get("unassigned") is None:
            return ErrorResponse(
                APIerror(
                    "assigned-null", 
                    status.HTTP_400_BAD_REQUEST, 
                    "Translation state not specified."
                )
            )

        try:
            translations = Translation.objects.filter(
                interpreter__isnull=request.data["unassigned"],
                active=True
            )
            serializer = GetTranslationSerializer(translations, many=True)
            return APIresponse(serializer.data)

        except Exception as e:
            print(e)
            return INTERNAL_ERROR_RESPONSE
        

class TranslationRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file_data = request.data.pop('document')
        file_format, file_content = file_data.split(';base64,')  
        file_obj = ContentFile(base64.b64decode(file_content), name=request.data["document_name"])
        request.data["document"] = file_obj
        request.data["customer"] = request.user.customer
        serializer = CreateTranslationSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            serializer.save(customer=request.user.customer)
            
            return Response(
                {
                    "message": "Translation requested successfully!"
                },
                status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class TranslationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        translations = Translation.objects.filter(customer=request.user.customer)
        serializer = GetTranslationSerializer(translations, many=True)

        return APIresponse(
            {"result": serializer.data},
        )
    
class OfferedTranslationsView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def post(self, request, *args, **kwargs):
        try:
            token = request.COOKIES.get('authToken')
            user = get_user_from_token(token)
            user, user_type = get_full_user(user)
            
            appointments = Translation.objects.filter(offered_to=user)
            serializer = GetTranslationSerializer(appointments, many=True)
            return APIresponse(serializer.data)
        
        except Exception as e:
            print(e)
            return INTERNAL_ERROR_RESPONSE
    
class TranslationOfferingResponse(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]
    
    def post(self, request):
        data = request.data
        expected = [
            "translationID",
            "accepted",
        ]

        if all(data[attr] is not None for attr in expected):
            try:
                translation = Translation.objects.get(id=data["translationID"])
                token = request.COOKIES.get('authToken')
                user = get_user_from_token(token)
                user, user_type = get_full_user(user)
                
                if data["accepted"]:
                    translation.offered_to.clear()
                    translation.interpreter = user
                    translation.save()
                else:
                    translation.offered_to.remove(user)
                return APIresponse({"message": "Offering successfully accepted."})
            
            except Exception:
                print("Exception occurred:", traceback.format_exc())
                return ErrorResponse(
                    APIerror(
                        "acceptance-error", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in translation."
                    )
                )
        else:
            return ErrorResponse(
                APIerror(
                    "appointment-errors", 
                    status.HTTP_400_BAD_REQUEST, 
                    "Errors in translation. Unexpected None attributes"
                )
            )
    
class TranslationAcceptanceView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def post(self, request, translation_id):
        try:
            translation = Translation.objects.get(id=translation_id)
            accepted = request.data.get("accepted", False)

            if accepted:
                translation.status = "Accepted"
            else:
                translation.status = "Declined"
            translation.save()
            return Response({"message": "Appointment status updated."}, status.HTTP_200_OK)
        except Translation.DoesNotExist:
            return Response({"error": "Appointment not found."}, status.HTTP_404_NOT_FOUND)


class UpdateTranslationOffering(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request):
        data = request.data
        expected = [
            "translationID",
            "interpreterID",
            "offer"
        ]
        
        if all(data[attr] is not None for attr in expected):

            try:
                translation = Translation.objects.get(id=data["translationID"])
                interpreter = Interpreter.objects.get(id=data["interpreterID"])
                
                if data["offer"]:
                    translation.offered_to.add(interpreter)
                else:
                    translation.offered_to.remove(interpreter)

                return APIresponse({"message": "Translation offering updated."})
            
            except Exception:
                return ErrorResponse(
                    APIerror(
                        "offer-errors", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in offering translation."
                    )
                )

        return ErrorResponse(
            APIerror(
                "offer-errors", 
                status.HTTP_400_BAD_REQUEST, 
                "Errors in offer inputs."
            )
        )
    
class ToggleTranslationInvoiceAppView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request):
        data = request.data
        
        if data["translationID"] is not None:

            try:
                translation = Translation.objects.get(id=data["translationID"])
                translation.invoice_generated = not translation.invoice_generated
                translation.save()
                return APIresponse({"message": "Translation invoice generated updated."})
            
            except Exception:
                return ErrorResponse(
                    APIerror(
                        "offer-errors", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in toggling translation invoice."
                    )
                )

        return ErrorResponse(
            APIerror(
                "offer-errors", 
                status.HTTP_400_BAD_REQUEST, 
                "Errors in app ID input."
            )
        )
    
class FetchInterpreterAcceptedTranslations(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def post(self, request):
        try:
            token = request.COOKIES.get('authToken')
            user = get_user_from_token(token)
            user, user_type = get_full_user(user)
            
            appointments = Translation.objects.filter(interpreter=user)
            serializer = GetTranslationSerializer(appointments, many=True)
            return APIresponse(serializer.data)
        
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE
        
class SetTranslationActualWordCount(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def post(self, request):

        translationID = request.data.get("translationID")
        actual_word_count = request.data.get("actualWordCount")

        translation_id_failure_error = ErrorResponse(
            APIerror(
                "id-error", 
                status.HTTP_400_BAD_REQUEST, 
                "Translation id invalid."
            )
        )

        if not isinstance(translationID, int):
            return translation_id_failure_error

        try:
            translation = Translation.objects.get(id=translationID)
            translation.actual_word_count = actual_word_count
            translation.save()
            return APIresponse({"message": "Translation actual word count set"})
        except Translation.DoesNotExist:
            return translation_id_failure_error
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE