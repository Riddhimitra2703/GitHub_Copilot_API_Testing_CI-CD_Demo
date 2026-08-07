"""Create user tests.

This file validates the POST create-user workflow for the ReqRes API using a shared
request context, JSON payload data, and JSON Schema validation for the response.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import allure
import pytest
from playwright.sync_api import APIRequestContext

from utils.test_data import CREATE_USER_ENDPOINT, STATUS_CREATED, validate_response_schema


@pytest.mark.smoke
@pytest.mark.crud
@allure.title("Create a user")
@allure.description("POST a user payload to the ReqRes API and validate the response schema.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "post", "create-user")
def test_create_user(api_request_context: APIRequestContext, logger: logging.Logger) -> None:
    """Create a new user and validate the response shape against the schema."""
    payload = json.loads((Path(__file__)
                          .resolve().parents[1] / "test_data" / "create_user_data.json")
                          .read_text(encoding="utf-8"))

    response = api_request_context.post(CREATE_USER_ENDPOINT, data=payload)
    logger.info("POST %s -> %s", CREATE_USER_ENDPOINT, response.status)
    logger.info("Request payload: %s", payload)
    logger.info("Response body: %s", response.text())

    assert response.status == STATUS_CREATED
    response_body = response.json()
    validate_response_schema(response_body, "create_user_schema.json")
