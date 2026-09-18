import pytest
from pydantic import ValidationError


def validate_schema(schema, data):
    try:
        if isinstance(data, list):
            for item in data:
                schema.model_validate(item)
        else:
            schema.model_validate(data)
    except ValidationError as e:
        pytest.fail(f"Ошибка валидации модели pydantic: {e}")
