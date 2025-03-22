import json 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
import traceback

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = APIerror("other-error", response.status_code, 
                                 response.data["detail"]).dict()

        if isinstance(exc, APIerror):
            response.data["error-code"] = exc.get_codes()

            if exc.get_codes() == "not_authenticated":
                response.data["error-code"] = "not-authenticated"
                response.data["error-message"] = "You must be logged in to complete this action."
            else:
                print(traceback.print_exception(exc))

        if isinstance(exc, AuthenticationFailed):
            if hasattr(context['request'], '_auth_failed_response'):
                response = context['request']._auth_failed_response
    else:
        print(traceback.print_exception(exc))
        response = INTERNAL_ERROR_RESPONSE
    
    response.data["status"] = "error"
        
    return response

class APIresponse(Response):
    def __init__(self, response_data, http_code=status.HTTP_200_OK):
        super().__init__()
        self.status = "success"
        self.response_data = response_data
        self.data = self.dict()
        self.status_code = http_code

    def dict(self):
        return {
            "status": self.status,
            "result": self.response_data
        }
    
    def __dict__(self):
        return self.dict()
    
    def json(self):
        return json.dumps(self.dict())

class APIerror:
    def __init__(self, error_code, error_http_code, error_message, 
                 error_data=None, error_list=None):
        self.code = error_code
        self.http_code = error_http_code
        self.error_message = error_message
        self.error_data = error_data
        self.error_list = error_list
    
    def dict(self):
        result = {
            "error-code": self.code,
            "error-http-code": self.http_code,
            "error-message": self.error_message
        }

        if self.error_list is not None:
            result["error-list"] = self.error_list

        if self.error_data is not None:
            result["error-data"] = self.error_data
        
        return result

class ErrorResponse(APIresponse):
    def __init__(self, error):
        if (not isinstance(error, APIerror)):
            raise ValueError("error not an APIerror")
        
        self.status_code = error.http_code
        self.error = error

        self.status = "error"
        self.data = self.dict()
        
        super().__init__(self.data, self.status_code)

        # Repeated so that status is correctly set after init
        self.status = "error"
        self.data = self.dict()
    
    def dict(self):
        return {
            "status": self.status,
            "error": self.error.dict()
        }


INTERNAL_ERROR_RESPONSE = ErrorResponse(
    APIerror(
        "django-error", 
        status.HTTP_500_INTERNAL_SERVER_ERROR, 
        "Unknown Django error"
           )
           )