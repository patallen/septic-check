from functools import wraps

from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import HttpRequest, HttpResponseNotAllowed, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods

from api.gateway import HouseCanaryApi
from api.response import render_usecase_response, render_validation_response
from api.usecase import CheckSeptic
from api.validators import ValidationError, validate_arguments


def require_http_methods_async(request_method_list):
    """
    Decorator to make a view only accept particular request methods.  Usage::
        @require_http_methods(["GET", "POST"])
        def my_view(request):
            # I can assume now that only GET or POST requests make it this far
            # ...
    Note that request methods should be in uppercase.

    **Note2: Code copied and adapted from django.views.decorator.http.require_http_methods
    """

    def decorator(func):
        @wraps(func)
        async def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                response = HttpResponseNotAllowed(request_method_list)
                log_response(
                    "Method Not Allowed (%s): %s",
                    request.method,
                    request.path,
                    response=response,
                    request=request,
                )
                return response
            return await func(request, *args, **kwargs)

        return inner

    return decorator


@require_http_methods_async(["GET"])
async def check_septic(request: HttpRequest, *_args, **_kwargs) -> JsonResponse:
    """
    Determines whether or not a property has a septic system installed.

    The following query parameters are required: address, zipcode.

    Status Code Meaning:
    ---
    200 -> Request completed successfully and true/false determination was made
    204 -> Request completed successfully; but true/false determination could not be made
    400 -> Request was improperly formatted or has an invalid set of arguments
    500 -> Request failed due internal error: I.e. Could not connect to external API

    Response Formats
    ---
    200 OK:
        Content-Type: application/json
        {"result": <bool>}

    non-200 OK:
        Content-Type: application/json
        {"message": <string>, "data": [<supporting datas>]}

    Example:
        GET /check-septic?address=18 Haskell Rd&zipcode=03087
        => 200 OK
        Content-Type: application/json
        {"result": true}
    """

    try:
        arguments = validate_arguments(request.GET)
    except ValidationError as error:
        return render_validation_response(error)

    api = HouseCanaryApi(
        base_url=settings.HOUSE_CANARY_BASE_URL,
        api_key=settings.HOUSE_CANARY_API_KEY,
        api_secret=settings.HOUSE_CANARY_API_SECRET,
    )

    use_case = CheckSeptic(house_canary_api=api)
    uc_request = use_case.Request.from_dict(arguments)
    result = await use_case.execute(uc_request)

    return render_usecase_response(result)
