from django.test import SimpleTestCase

from api.validators import validate_arguments, ValidationError


class ValidationTests(SimpleTestCase):
    def test_validate_arguments_with_valid_inputs(self):
        arguments = {"zipcode": "90210", "address": "100 One Hundred Dr."}

        validated = validate_arguments(arguments)
        self.assertDictEqual(arguments, validated)

    def test_validate_arguments_with_missing(self):
        arguments = {"zipcode": "90210"}

        with self.assertRaises(ValidationError) as context:
            _ = validate_arguments(arguments)

        self.assertEqual(context.exception.message, "missing required arguments")
        self.assertEqual(context.exception.fields, ["address"])

    def test_validate_arguments_with_empty_arguments_raises(self):
        arguments = {}

        with self.assertRaises(ValidationError) as context:
            _ = validate_arguments(arguments)

        self.assertEqual(context.exception.message, "missing required arguments")
        self.assertEqual(context.exception.fields, ["address", "zipcode"])

    def test_validate_arguments_with_extra_keys_raises(self):
        arguments = {
            "zipcode": "90210",
            "address": "100 One Hundred Dr.",
            "extra_key": "this is extra",
        }

        with self.assertRaises(ValidationError) as context:
            _ = validate_arguments(arguments)

        self.assertEqual(context.exception.message, "invalid arguments")
        self.assertEqual(context.exception.fields, ["extra_key"])
