from django.test import SimpleTestCase

from api.tests.mocks import MockHouseCanaryApi
from api.usecase import CheckSeptic, CheckSepticRequest
from api import interface


class UseCaseTests(SimpleTestCase):
    gateway = MockHouseCanaryApi(
        {
            ("10 Gotham Manor", "53540"): {"sewer": "Septic"},
            ("9390 Readcrest Dr", "90210"): {"sewer": "municipal"},
            ("22 no data dr", "00000"): {},
        }
    )

    def test_use_case_not_found(self):
        use_case = CheckSeptic(self.gateway)

        request = CheckSepticRequest(address="this is no address", zipcode="92010")
        response = use_case.execute(request)

        self.assertTrue(response.has_error())
        self.assertEquals(response.error_type, interface.NOT_FOUND_ERROR)
        self.assertIsNone(response.result)

    def test_use_case_found_not_septic(self):
        use_case = CheckSeptic(self.gateway)

        request = CheckSepticRequest(address="9390 Readcrest Dr", zipcode="90210")
        response = use_case.execute(request)

        self.assertFalse(response.has_error())
        self.assertIsNone(response.error_type)
        self.assertFalse(response.result)

    def test_use_case_found_has_septic(self):
        use_case = CheckSeptic(self.gateway)

        request = CheckSepticRequest(address="10 Gotham Manor", zipcode="53540")
        response = use_case.execute(request)

        self.assertFalse(response.has_error())
        self.assertIsNone(response.error_type)
        self.assertTrue(response.result)

    def test_use_case_insufficient_data(self):
        use_case = CheckSeptic(self.gateway)

        request = CheckSepticRequest(address="22 no data dr", zipcode="00000")
        response = use_case.execute(request)

        self.assertTrue(response.has_error())
        self.assertEquals(response.error_type, interface.NO_DATA_ERROR)
        self.assertIsNone(response.result)
