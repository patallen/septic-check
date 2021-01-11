from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.http import response

from api.validators import validate_arguments, ValidationError
from api.external import HouseCanaryApi, NotFoundError, UnknownError


class CheckHomeHasSeptic(View):
    def get(self, request: HttpRequest, *_args, **_kwargs) -> JsonResponse:
        """
        Determines whether or not a property has a septic system installed.

        The following query parameters are required: address, zipcode.

        Status Code Meaning:
        ---
        200 -> Request completed successfully and true/false determination was made
        204 -> Request completed successfully, but true/false determination could not be made
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
            return response.JsonResponse(
                {"message": error.message, "data": error.fields}, status=400
            )

        api = HouseCanaryApi(
            base_url=settings.HOUSE_CANARY_BASE_URL,
            api_key=settings.HOUSE_CANARY_API_KEY,
            api_secret=settings.HOUSE_CANARY_API_SECRET,
        )

        try:
            home_details = api.fetch_home_details(**arguments)
        except NotFoundError:
            return JsonResponse({"message": "property not found"}, status=204)
        except UnknownError:
            return JsonResponse({"message": "an unknown error occurred"}, status=500)

        try:
            sewer_info = home_details["sewer"]
        except KeyError:
            return JsonResponse(status=204)

        has_septic = sewer_info and sewer_info.lower() == "septic"
        return JsonResponse({"result": has_septic})
