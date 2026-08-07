"""Reusable constants and shared validation helpers for the ReqRes API suite.

This module centralizes endpoint paths, supported status codes, and schema validation
logic so the tests stay consistent and free from repeated inline definitions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATA_DIR = PROJECT_ROOT / "test_data"
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"

LIST_USERS_ENDPOINT = "/api/users"
SINGLE_USER_ENDPOINT = "/api/users/{user_id}"
CREATE_USER_ENDPOINT = "/api/users"
UPDATE_USER_ENDPOINT = "/api/users/{user_id}"
DELETE_USER_ENDPOINT = "/api/users/{user_id}"

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NO_CONTENT = 204
STATUS_NOT_FOUND = 404


def load_json_file(file_path: str | Path) -> Any:
    """Load a JSON file from disk.

    Args:
        file_path: Path-like value pointing to the JSON file.

    Returns:
        Parsed JSON content.
    """
    with Path(file_path).open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_response_schema(response_data: Any, schema_name: str) -> None:
    """Validate a payload against a JSON Schema document.

    Args:
        response_data: Parsed API response payload to validate.
        schema_name: The schema filename stored under utils/schemas.
    """
    schema = load_json_file(SCHEMA_DIR / schema_name)
    validate(instance=response_data, schema=schema)
