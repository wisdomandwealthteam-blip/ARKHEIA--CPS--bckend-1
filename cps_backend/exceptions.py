class SchemaValidationError(ValueError):
    """Raised when a rule set fails schema validation."""


class StateNotSupportedError(ValueError):
    """Raised when a requested state is not in SUPPORTED_STATES."""
