class ResponseMock:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        return self._json


def mocked_requests_get(*args, **kwargs):
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


def mocked_requests_get_internal_error(*args, **kwargs):
    return ResponseMock(500)


def mocked_requests_get_no_content(*args, **kwargs):
    return ResponseMock(204)
