import abc

NOT_FOUND_ERROR = "NOT_FOUND"
UNKNOWN_ERROR = "UNKNOWN_ERROR"
NO_DATA_ERROR = "INSUFFICIENT_DATA"


class UnknownError(Exception):
    """Raised when an unknown error response is received"""


class NotFoundError(Exception):
    """Raised when an entity does not exist or cannot be found"""


class AbstractHouseCanaryApi(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch_home_details(self, address: str, zipcode: str) -> dict:
        pass
