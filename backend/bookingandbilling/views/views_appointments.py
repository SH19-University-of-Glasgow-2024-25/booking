from bookingandbilling.serializers.model_serializers import (
    GetAppointmentSerializer,
    InterpreterSerializer,
    
)

from bookingandbilling.serializers.appointment_serializers import (
    CreateAppointmentSerializer
)

from ..email_utils import send_appointment_accepted_email, send_appointment_offered_email

from ..models import AccountType, Appointment, Interpreter
from .views_utility import IsUserType, get_full_user, get_user_from_token
from rest_framework.views import APIView
from ..utilities import (
    APIerror,
    APIresponse,
    INTERNAL_ERROR_RESPONSE,
    ErrorResponse
)
from rest_framework import status
from datetime import datetime
import traceback
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class FetchAppointmentsView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request, *args, **kwargs):
        if request.data.get("unassigned") is None:
            return ErrorResponse(
                APIerror(
                    "assigned-null", 
                    status.HTTP_400_BAD_REQUEST, 
                    "Assignment state not specified."
                )
            )

        try:
            appointments = Appointment.objects.filter(
                interpreter__isnull=request.data["unassigned"],
                active=True
            ).order_by("planned_start_time")
            serializer = GetAppointmentSerializer(appointments, many=True)
            return APIresponse(serializer.data)
        
        except Exception as e:
            print(e)
            return INTERNAL_ERROR_RESPONSE

class OfferedAppointmentsView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def post(self, request, *args, **kwargs):
        try:
            token = request.COOKIES.get('authToken')
            user = get_user_from_token(token)
            user, user_type = get_full_user(user)
            
            appointments = Appointment.objects.filter(
                offered_to=user).order_by("planned_start_time")
            serializer = GetAppointmentSerializer(appointments, many=True)
            return APIresponse(serializer.data)
        
        except Exception as e:
            print(e)
            return INTERNAL_ERROR_RESPONSE        

class AllInterpretersView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def get(self, request, *args, **kwargs):
        try:
            interpreters = Interpreter.objects.filter()
            serializer = InterpreterSerializer(interpreters, many=True)
            return APIresponse(serializer.data)
        
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE

class AppointmentRequestView(APIView):
    permission_classes = [IsAuthenticated]
   
    def post(self, request):
        request.data["customer"] = request.user.customer
        serializer = CreateAppointmentSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {  
                    "message": "Appointment requested successfully!"
                },
                status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
   
class AppointmentsView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        appointments = Appointment.objects.filter(
            customer=request.user.customer).order_by("planned_start_time")
        serializer = GetAppointmentSerializer(appointments, many=True)
        return APIresponse(
            {"result": serializer.data},
        )
   
class AppointmentAcceptanceView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]
 
    def post(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            accepted = request.data.get("accepted", False)
 
            if accepted:
                appointment.status = "Accepted"
            else:
                appointment.status = "Declined"
           
            appointment.save()
            return Response({"message": "Appointment status updated."}, status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status.HTTP_404_NOT_FOUND)
        

class UpdateAppointmentOffering(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request):
        data = request.data
        expected = [
            "appID",
            "interpreterID",
            "offer"
        ]
        
        if all(data[attr] is not None for attr in expected):

            try:
                appointment = Appointment.objects.get(id=data["appID"])
                interpreter = Interpreter.objects.get(id=data["interpreterID"])
                
                if data["offer"]:
                    appointment.offered_to.add(interpreter)
                    send_appointment_offered_email(appointment, interpreter)
                else:
                    appointment.offered_to.remove(interpreter)

                return APIresponse({"message": "Appointment offering updated."})
            
            except Exception:
                return ErrorResponse(
                    APIerror(
                        "offer-errors", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in offering appointment."
                    )
                )

        return ErrorResponse(
            APIerror(
                "offer-errors", 
                status.HTTP_400_BAD_REQUEST, 
                "Errors in offer inputs."
            )
        )
                
class UpdateInterpreterOffering(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]
    
    def post(self, request):
        data = request.data
        expected = [
            "appID",
            "accepted",
        ]

        if all(data[attr] is not None for attr in expected):
            try:
                appointment = Appointment.objects.get(id=data["appID"])
                token = request.COOKIES.get('authToken')
                user = get_user_from_token(token)
                user, user_type = get_full_user(user)
                if data["accepted"]:
                    appointment.offered_to.clear()
                    appointment.interpreter = user
                    send_appointment_accepted_email(appointment, appointment.customer)
                    appointment.save()
                else:
                    appointment.offered_to.remove(user)
                return APIresponse({"message": "Offering successfully accepted."})
            except Exception:
                print("Exception occurred:", traceback.format_exc())
                return ErrorResponse(
                    APIerror(
                        "acceptance-error", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in appointment."
                    )
                )
        else:
            return ErrorResponse(
                APIerror(
                    "appointment-errors", 
                    status.HTTP_400_BAD_REQUEST, 
                    "Errors in appointment. Unexpected None attributes"
                )
            )
        
class AcceptedAppointments(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def get(self, request, *args, **kwargs):

        try:

            token = request.COOKIES.get('authToken')
            user = get_user_from_token(token)
            user, user_type = get_full_user(user)
            appointments = Appointment.objects.filter(
                interpreter=user).order_by("planned_start_time")
            serializer = GetAppointmentSerializer(appointments, many=True)
            return APIresponse(serializer.data)
        
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE

class EditAppointments(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.INTERPRETER])]

    def post(self, request):
        data = request.data

        if data["appID"] is not None:
            try:
                appointment = Appointment.objects.get(id=data["appID"])
                
                try:
                    updated_time = datetime.strptime(data["appActualStartTime"], "%H:%M").time()
                    valid_time = timezone.make_aware(updated_time, timezone.get_current_timezone())
                    appointment.actual_start_time = datetime.combine(
                        appointment.planned_start_time.date(), valid_time
                    )
                except Exception:
                    if data["appActualStartTime"] == "":
                        appointment.actual_start_time = None

                try:
                    appointment.actual_duration = datetime.strptime(
                        data["appActualDuration"], "%H:%M"
                    )
                except Exception:
                    if data["appActualDuration"] == "":
                        appointment.actual_duration = None
                appointment.save()
            except Exception:
                print("Exception occurred:", traceback.format_exc())
                return ErrorResponse(
                    APIerror(
                        "acceptance-error", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in appointment editing."
                    )
                )
        return APIresponse({"message": "Appointment successfully edited"})
    
class ToggleAppointmentInvoiceAppView(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]

    def post(self, request):
        data = request.data
        
        if data["appID"] is not None:

            try:
                appointment = Appointment.objects.get(id=data["appID"])
                appointment.invoice_generated = not appointment.invoice_generated
                appointment.save()
                return APIresponse({"message": "Appointment invoice generated updated."})
            
            except Exception:
                return ErrorResponse(
                    APIerror(
                        "offer-errors", 
                        status.HTTP_400_BAD_REQUEST, 
                        "Errors in toggling appointment invoice."
                    )
                )

        return ErrorResponse(
            APIerror(
                "offer-errors", 
                status.HTTP_400_BAD_REQUEST, 
                "Errors in app ID input."
            )
        )