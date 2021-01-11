from unittest import mock

from django.test import SimpleTestCase

from api.gateway import HouseCanaryApi
from api.interface import NotFoundError, UnknownError
from api.tests.mocks import (
    mocked_requests_get,
    mocked_requests_get_internal_error,
    mocked_requests_get_no_content,
)


class HouseCanaryApiTests(SimpleTestCase):
    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_requests_get_called_properly(self, mocked_get: mock.Mock):
        api = HouseCanaryApi("https://example.com", "api_key", "secret")
        _ = api.fetch_home_details("21 Flint st", "02145")
        mocked_get.assert_called_with(
            "https://example.com/property/details",
            auth=("api_key", "secret"),
            params={"address": "21 Flint st", "zipcode": "02145"},
        )

    def test_build_url_generates_correct_url(self):
        api = HouseCanaryApi("https://example.com", "", "")
        url = api.build_url()
        self.assertEqual(url, "https://example.com/property/details")

    def test_build_url_with_trailing_slash_generates_correct_url(self):
        api = HouseCanaryApi("https://example.com/", "", "")
        url = api.build_url()
        self.assertEqual(url, "https://example.com/property/details")

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_fetch_home_details_returns_only_property_details(self, _mocked_get):
        api = HouseCanaryApi("https://example.com/", "", "")
        url = api.build_url()
        self.assertEqual(url, "https://example.com/property/details")

    @mock.patch("requests.get", side_effect=mocked_requests_get_no_content)
    def test_fetch_home_details_raises_NotFoundError_for_204(self, _mocked_get):
        api = HouseCanaryApi("https://example.com/", "", "")
        with self.assertRaises(NotFoundError):
            _ = api.fetch_home_details("1000 doesn't exist", "90210")

    @mock.patch("requests.get", side_effect=mocked_requests_get_internal_error)
    def test_fetch_home_details_raises_NotFoundError_for_internal_error(
        self, _mocked_get
    ):
        api = HouseCanaryApi("https://example.com/", "", "")
        with self.assertRaises(UnknownError):
            _ = api.fetch_home_details("1000 doesn't exist", "90210")
