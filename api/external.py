import requests
import pathlib


class UnknownError(Exception):
    """Raised when an unknown error response is received"""


class NotFoundError(Exception):
    """Raised when an entity does not exist or cannot be found"""


class HouseCanaryApi:
    def __init__(self, base_url, api_key, api_secret, timeout=10):
        self._url = base_url
        self._timeout = timeout
        self._auth = (api_key, api_secret)

    def build_url(self):
        return f"{self._url.rstrip('/')}/property/details"

    def fetch_home_details(self, address, zipcode):
        url = self.build_url()
        params = {
            "address": address,
            "zipcode": zipcode,
        }
        response = requests.get(url, params=params, auth=self._auth)

        if response.status_code == 204:
            raise NotFoundError("property not found")

        if response.status_code != 200:
            raise UnknownError("an unknown error occurred")

        return response.json()
