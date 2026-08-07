"""Update user tests.

This module covers PUT and PATCH update flows using a shared API request context.
It validates the response payload against the update schema for both successful update
operations and common update variants.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import allure
import pytest
from playwright.sync_api import APIRequestContext

from utils.test_data import STATUS_OK, UPDATE_USER_ENDPOINT, validate_response_schema


@pytest.mark.regression
@pytest.mark.crud
@allure.title("Update user with PUT")
@allure.description("Send a PUT request to update an existing user and validate the JSON schema.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "put", "update-user")
def test_update_user_put(api_request_context: APIRequestContext, logger: logging.Logger) -> None:
    """Update a user with a PUT request and validate the response schema."""
    payload = json.loads((Path(__file__).resolve().parents[1] / "test_data" / "update_user_data.json").read_text(encoding="utf-8"))
    endpoint = UPDATE_USER_ENDPOINT.format(user_id=2)

    response = api_request_context.put(endpoint, data=payload)
    logger.info("PUT %s -> %s", endpoint, response.status)
    logger.info("Request payload: %s", payload)
    logger.info("Response body: %s", response.text())

    assert response.status == STATUS_OK
    response_body = response.json()
    validate_response_schema(response_body, "update_user_schema.json")


@pytest.mark.regression
@pytest.mark.crud
@allure.title("Update user with PATCH")
@allure.description("Send a PATCH request to partially update an existing user and validate the response schema.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "patch", "update-user")
def test_update_user_patch(api_request_context: APIRequestContext, logger: logging.Logger) -> None:
    """Update a user with a PATCH request and validate the response schema."""
    payload = {"name": "Morpheus Patch", "job": "Patch QA Engineer"}
    endpoint = UPDATE_USER_ENDPOINT.format(user_id=2)

    response = api_request_context.patch(endpoint, data=payload)
    logger.info("PATCH %s -> %s", endpoint, response.status)
    logger.info("Request payload: %s", payload)
    logger.info("Response body: %s", response.text())

    assert response.status == STATUS_OK
    response_body = response.json()
    validate_response_schema(response_body, "update_user_schema.json")
