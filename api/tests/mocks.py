from typing import Dict, List

from api.interface import AbstractHouseCanaryApi, NotFoundError


class ResponseMock:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json


def mocked_requests_get(*_args, **_kwargs):
    return ResponseMock(
        200,
        {
            "property/details": {
                "api_code_description": "ok",
                "api_code": 0,
                "result": {
                    "property": {
                        "sewer": "Septic",
                    },
                },
            }
        },
    )


def mocked_requests_get_internal_error(*_args, **_kwargs):
    return ResponseMock(500)


def mocked_requests_get_no_content(*_args, **_kwargs):
    return ResponseMock(204)


class MockHouseCanaryApi(AbstractHouseCanaryApi):
    def __init__(self, properties: List[Dict[str, str]]) -> None:
        self.properties = properties

    def fetch_home_details(self, address: str, zipcode: str) -> dict:
        composite_key = (address, zipcode)
        details = self.properties.get(composite_key)

        if details is None:
            raise NotFoundError("property not found")

        return details
