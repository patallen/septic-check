from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View

from api.gateway import HouseCanaryApi
from api.response import render_usecase_response, render_validation_response
from api.usecase import CheckSeptic
from api.validators import ValidationError, validate_arguments


class CheckHomeHasSeptic(View):
    def get(self, request: HttpRequest, *_args, **_kwargs) -> JsonResponse:
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
        result = use_case.execute(uc_request)

        return render_usecase_response(result)
