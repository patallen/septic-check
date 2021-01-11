from django.http import JsonResponse

from api import interface
from api.usecase import CheckSepticResponse
from api.validators import ValidationError

_ERROR_TYPE_TO_STATUS = {
    interface.NOT_FOUND_ERROR: (204, "property not found"),
    interface.NO_DATA_ERROR: (204, "no sewer data for property"),
    interface.UNKNOWN_ERROR: (500, "an unknown error occurred"),
}


def render_validation_response(error: ValidationError) -> JsonResponse:
    """Render a json response from a ValidationError instance"""

    return JsonResponse({"message": error.message, "data": error.fields}, status=400)


def render_usecase_response(result: CheckSepticResponse) -> JsonResponse:
    """Render a json response from a CheckSeptic usecase response object"""

    data = {}
    status_code = 200

    if result.has_error():
        status_code, message = _ERROR_TYPE_TO_STATUS[result.error_type]
        data["message"] = message
    else:
        data["result"] = result.result

    return JsonResponse(data, status=status_code)
