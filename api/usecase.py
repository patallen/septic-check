from dataclasses import dataclass
from typing import Optional

from api import interface


@dataclass
class CheckSepticRequest:
    address: str
    zipcode: str

    @classmethod
    def from_dict(cls, adict):
        return cls(**adict)


@dataclass
class CheckSepticResponse:
    error_type: Optional[str] = None
    result: Optional[bool] = None

    def has_error(self):
        return self.error_type is not None


class CheckSeptic:
    Request = CheckSepticRequest

    def __init__(self, house_canary_api: interface.AbstractHouseCanaryApi) -> None:
        self.house_canary = house_canary_api

    async def execute(self, request: CheckSepticRequest) -> CheckSepticResponse:
        """Determine if property for address described within :request: has a septic system."""

        try:
            home_details = await self.house_canary.fetch_home_details(
                request.address, request.zipcode
            )
        except interface.NotFoundError:
            return CheckSepticResponse(error_type=interface.NOT_FOUND_ERROR)
        except interface.UnknownError:
            return CheckSepticResponse(error_type=interface.UNKNOWN_ERROR)

        sewer_info = home_details.get("sewer")
        if not sewer_info:
            return CheckSepticResponse(error_type=interface.NO_DATA_ERROR)

        has_septic = sewer_info.lower() == "septic"
        return CheckSepticResponse(result=has_septic)
