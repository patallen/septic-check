from django.views import View

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