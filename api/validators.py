VALID_QUERY_PARAMETERS = ("address", "zipcode")


class ValidationError(Exception):
    def __init__(self, message, fields):
        self.message = message
        self.fields = fields


def validate_arguments(arguments: dict) -> dict:
    missing_fields = [
        field for field in VALID_QUERY_PARAMETERS if field not in arguments
    ]
    extra_fields = [field for field in arguments if field not in VALID_QUERY_PARAMETERS]

    if missing_fields:
        raise ValidationError(f"missing required arguments", missing_fields)

    if extra_fields:
        raise ValidationError(f"invalid arguments", extra_fields)

    return {field: arguments[field] for field in VALID_QUERY_PARAMETERS}
