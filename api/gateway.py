import httpx

from api import interface


async def async_fetch(url, params, auth, timeout):
    async with httpx.AsyncClient() as client:
        return await client.get(url, params=params, auth=auth, timeout=timeout)


class HouseCanaryApi(interface.AbstractHouseCanaryApi):
    def __init__(
        self, base_url: str, api_key: str, api_secret: str, timeout: int = 10
    ) -> None:
        self._url = base_url
        self._timeout = timeout
        self._auth = (api_key, api_secret)

    def build_url(self) -> str:
        """Build and return the HouseCanary property/details url"""

        return f"{self._url.rstrip('/')}/property/details"

    async def fetch_home_details(self, address: str, zipcode: str) -> dict:
        """Pull property-level data for a property from HouseCanary web API"""

        url = self.build_url()

        params = {
            "address": address,
            "zipcode": zipcode,
        }

        try:
            response = await async_fetch(
                url, params=params, auth=self._auth, timeout=self._timeout
            )
        except httpx.RequestError:
            raise interface.UnknownError("an unknown error occurred")

        if response.status_code == 204:
            raise interface.NotFoundError("property not found")

        if response.status_code != 200:
            raise interface.UnknownError("an unknown error occurred")

        return response.json()["property/details"]["result"]["property"]
