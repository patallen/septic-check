from unittest import mock

from django.test import SimpleTestCase

from api.tests.mocks import (
    mocked_requests_get_internal_error,
    mocked_requests_get_no_content,
    mocked_requests_get,
)


class CheckSepticViewTests(SimpleTestCase):
    def test_missing_params_error_response(self):
        response = self.client.get("/check-septic?address=10 Marley Way")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {"message": "missing required arguments", "data": ["zipcode"]},
        )

        response = self.client.get("/check-septic")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {"message": "missing required arguments", "data": ["address", "zipcode"]},
        )

    def test_extra_params_error_response(self):
        response = self.client.get(
            "/check-septic?address=10 Marley Way&zipcode=00000&pool=yes"
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(
            response.json(),
            {"message": "invalid arguments", "data": ["pool"]},
        )

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_external_has_septic(self, _mock_get):
        response = self.client.get("/check-septic?address=10 Marley Way&zipcode=00000")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["result"])

    @mock.patch("requests.get", side_effect=mocked_requests_get_no_content)
    def test_external_no_property_found(self, _mock_get):
        response = self.client.get("/check-septic?address=10 Marley Way&zipcode=00000")
        self.assertEqual(response.status_code, 204)

    @mock.patch("requests.get", side_effect=mocked_requests_get_no_content)
    def test_external_no_property_found(self, _mock_get):
        response = self.client.get("/check-septic?address=10 Marley Way&zipcode=00000")
        self.assertEqual(response.status_code, 204)

    @mock.patch("requests.get", side_effect=mocked_requests_get_internal_error)
    def test_external_no_property_found(self, _mock_get):
        response = self.client.get("/check-septic?address=10 Marley Way&zipcode=00000")
        self.assertEqual(response.status_code, 500)
