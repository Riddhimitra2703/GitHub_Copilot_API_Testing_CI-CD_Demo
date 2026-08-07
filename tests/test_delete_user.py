"""Delete user tests.

This module verifies the DELETE user endpoint using the shared API request context and
asserts the expected success status for a valid removal request.
"""

from __future__ import annotations

import logging

import allure
import pytest
from playwright.sync_api import APIRequestContext

from utils.test_data import DELETE_USER_ENDPOINT, STATUS_NO_CONTENT, STATUS_NOT_FOUND


@pytest.mark.smoke
@pytest.mark.crud
@allure.title("Delete an existing user")
@allure.description("Delete a valid user record and assert the expected no-content response.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "delete", "user")
def test_delete_user(api_request_context: APIRequestContext, logger: logging.Logger) -> None:
    """Delete an existing user from the ReqRes API."""
    endpoint = DELETE_USER_ENDPOINT.format(user_id=2)

    response = api_request_context.delete(endpoint)
    logger.info("DELETE %s -> %s", endpoint, response.status)
    logger.info("Response body: %s", response.text())

    assert response.status == STATUS_NO_CONTENT


@pytest.mark.regression
@pytest.mark.crud
@allure.title("Delete a non-existent user")
@allure.description("Verify the live ReqRes behavior for deleting a user that does not exist.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "delete", "missing-user")
def test_delete_missing_user(api_request_context: APIRequestContext, logger: logging.Logger) -> None:
    """Delete a user that does not exist and confirm the actual API contract."""
    endpoint = DELETE_USER_ENDPOINT.format(user_id=9999)

    response = api_request_context.delete(endpoint)
    logger.info("DELETE %s -> %s", endpoint, response.status)
    logger.info("Response body: %s", response.text())

    assert response.status == STATUS_NO_CONTENT
