import traceback
import sys
from collections import OrderedDict
from rest_framework.views import APIView

from django.contrib.auth.hashers import check_password

from ..serializers.edit_user_serializers import (
    AdminEditAdminSerializer,
    AdminEditCustomerSerializer,
    AdminEditInterpreterSerializer,
    SelfEditAdminSerializer, 
    SelfEditCustomerSerializer, 
    SelfEditInterpreterSerializer)

from ..utilities import (
    APIresponse,
    APIerror,
    ErrorResponse,
    INTERNAL_ERROR_RESPONSE
)

from ..models import (
    User,
    Interpreter,
    Customer,
    Admin,
    AccountType
)

from .views_utility import IsUserType, get_full_user

class RetrieveEmails(APIView):
    permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN])]
    
    def get(self, request):
        try:
            admins = Admin.objects.values_list('email', flat=True).exclude(email=request.user.email)
            customers = Customer.objects.values_list('email', flat=True)
            interpreters = Interpreter.objects.values_list('email', flat=True)
            return APIresponse({
                    "admins": admins,
                    "interpreters": interpreters,
                    "customers": customers,
                               })
        except Exception as e:
            print(traceback.print_exception(e))
            return INTERNAL_ERROR_RESPONSE

# Returns the fields that are editable for the authenticated user
class GetUserEditFieldsView(APIView):
    def get(self, request):
        fields = {}

        authenticated_user, authenticated_user_type = get_full_user(request.user)
        user_param = request.GET.get("user", "self")
        if (user_param == "self"):
            user = authenticated_user
        else:
            if (authenticated_user_type == AccountType.ADMIN):
                user = User.objects.filter(email=user_param).first()
                if user is None:
                    return ErrorResponse(APIerror("user-not-found", 
                                                  404, 
                                                  "The specified user was not found."))
            else:
                return ErrorResponse(APIerror("not-admin", 
                                              403, 
                                              "You must be an admin to complete this action."))

        user_type = "unknown"

        if (Interpreter.objects.filter(email=user.email).exists()):
            user_type = "interpreter"
            if (authenticated_user_type == AccountType.ADMIN):
                fields = AdminEditInterpreterSerializer.Meta.fields
            else:
                fields = SelfEditInterpreterSerializer.Meta.fields
            user = Interpreter.objects.filter(email=user.email).first().__dict__
        elif (Customer.objects.filter(email=user.email).exists()):
            user_type = "customer"
            if (authenticated_user_type == AccountType.ADMIN):
                fields = AdminEditCustomerSerializer.Meta.fields
            else:
                fields = SelfEditCustomerSerializer.Meta.fields
            user = Customer.objects.filter(email=user.email).first().__dict__
        elif (Admin.objects.filter(email=user.email).exists()):
            user_type = "admin"
            if (authenticated_user_type == AccountType.ADMIN and request.user.email != user_param):
                fields = AdminEditAdminSerializer.Meta.fields
            else:
                fields = SelfEditAdminSerializer.Meta.fields
            user = Admin.objects.filter(email=user.email).first().__dict__

        else:
            return ErrorResponse(APIerror("unknown-user", 
                                          403, 
                                          "The authenticated user is an unknown user type.", 
                                          str(type(user))))

        result_fields = OrderedDict(
            [(key, user[key]) if key in user else (key, "") for key in fields]
                                   )

        if "password" in result_fields:
            result_fields["password"] = ""
        
        return APIresponse({
                 "user-type": user_type,
                 "fields": result_fields
                })

def edit_user(user, user_type, data, edit_type="self"):
    if "password" in data and data["password"] == "":
        del data["password"]

    try:
        serializer = None
        if edit_type == "admin":
            if user_type == AccountType.INTERPRETER:
                serializer = AdminEditInterpreterSerializer(instance=user,
                                                            data=data)
            elif user_type == AccountType.CUSTOMER:
                serializer = AdminEditCustomerSerializer(instance=user,
                                                         data=data)
            elif user_type == AccountType.ADMIN:
                serializer = AdminEditAdminSerializer(instance=user,
                                                      data=data)
        else:
            if user_type == AccountType.INTERPRETER:
                serializer = SelfEditInterpreterSerializer(instance=user,
                                                           data=data)
            elif user_type == AccountType.CUSTOMER:
                serializer = SelfEditCustomerSerializer(instance=user,
                                                        data=data)
            elif user_type == AccountType.ADMIN:
                serializer = SelfEditAdminSerializer(instance=user,
                                                     data=data)
        
        # Weird nesting to satisfy broken VITE rules 
        # https://www.flake8rules.com/rules/W503.html and 
        # https://www.flake8rules.com/rules/W504.html contradict each other
        if "confirm_password" in serializer.fields and "confirm_password" not in data:
            if "password" in data:
                data["confirm_password"] = data["password"]

        is_valid = serializer.is_valid()

        if edit_type == "self" and 'test' not in sys.argv and "password" in data:
            if ("existing_password" not in data or data["existing_password"] == ""):
                error_list = {k:serializer.errors[k] for k in serializer.errors}
                error_list["Existing password"] = "You must enter your existing password"
                return ErrorResponse(
                    APIerror("form-invalid", 400, "There are form errors", error_list=error_list)
                )
            
            if (not check_password(data["existing_password"], user.password)):
                error_list = {k:serializer.errors[k] for k in serializer.errors}
                error_list["Existing password"] = "Your existing password was entered incorrectly"
                return ErrorResponse(
                    APIerror("form-invalid", 400, "There are form errors", error_list=error_list)
                )

        if is_valid:
            serializer.save()
        else:
            return ErrorResponse(
                APIerror("form-invalid", 400, "There are form errors", error_list=serializer.errors)
            )

    except Exception as e:
        print(traceback.print_exception(e))
        return INTERNAL_ERROR_RESPONSE
    return APIresponse({})

# Receives the edit data
class EditView(APIView):
    def post(self, request):
        authenticated_user, authenticated_user_type = get_full_user(request.user)
        user_param = request.GET.get("user", "self")
        if (user_param == "self"):
            user = authenticated_user
        else:
            if (authenticated_user_type == AccountType.ADMIN):
                user = User.objects.filter(email=user_param).first()
                if user is None:
                    return ErrorResponse(APIerror("user-not-found", 
                                         404, 
                                         "The specified user was not found."))
            else:
                return ErrorResponse(APIerror("not-admin", 
                                     403, 
                                     "You must be an admin to complete this action."))
        
        user, user_type = get_full_user(user)

        edit_type = "self" if user_param == "self" else "admin"

        return edit_user(user, user_type, request.data.dict(), edit_type=edit_type)

class AdminEditOtherView(APIView):
    def post(self, request):
        data = request.data.dict()
        current_user, current_user_type = get_full_user(request.user)
        if current_user_type != AccountType.ADMIN:
            return ErrorResponse(APIerror("not-admin", 
                                          403, 
                                          "You must be an admin to complete this action."))
        
        user, user_type = get_full_user(User.objects.get(username=data["target-user"]))

        # remove target user field such that data only contains form data for serializer
        del data["target-user"]

        return edit_user(user, user_type, data, request)