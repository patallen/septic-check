import json

from django.test import SimpleTestCase
from django.http import JsonResponse

from api.response import render_validation_response, render_usecase_response
from api.usecase import CheckSepticResponse


class MockValidationError:
    def __init__(self, message, fields):
        self.message = message
        self.fields = fields


class RenderValidationResponseTests(SimpleTestCase):
    def test_render_validation_response(self):
        error = MockValidationError(message="missing required fields", fields=["name"])
        response = render_validation_response(error)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content,
            json.dumps({"message": "missing required fields", "data": ["name"]}).encode(
                "ascii"
            ),
        )
        self.assertEqual(response.status_code, 400)


class RenderUsecaseResponseTests(SimpleTestCase):
    def test_render_use_case_response_not_found(self):
        uc_response = CheckSepticResponse(error_type="NOT_FOUND")

        response = render_usecase_response(uc_response)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content,
            json.dumps({"message": "property not found",}).encode("ascii"),
        )
        self.assertEqual(response.status_code, 204)

    def test_render_use_case_response_no_data(self):
        uc_response = CheckSepticResponse(error_type="INSUFFICIENT_DATA")

        response = render_usecase_response(uc_response)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content,
            json.dumps({"message": "no sewer data for property",}).encode("ascii"),
        )
        self.assertEqual(response.status_code, 204)

    def test_render_use_case_response_unknown_error(self):
        uc_response = CheckSepticResponse(error_type="UNKNOWN_ERROR")

        response = render_usecase_response(uc_response)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(
            response.content,
            json.dumps({"message": "an unknown error occurred",}).encode("ascii"),
        )
        self.assertEqual(response.status_code, 500)
