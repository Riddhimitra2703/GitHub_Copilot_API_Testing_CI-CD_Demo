"""GET user tests.

This module verifies both list-user and single-user GET workflows using a shared
Playwright APIRequestContext and JSON Schema validation. It also exercises
positive and negative single-user lookup scenarios with a parametrized dataset.
"""

from __future__ import annotations

import logging

import allure
import pytest
from playwright.sync_api import APIRequestContext

from utils.test_data import (
    LIST_USERS_ENDPOINT,
    SINGLE_USER_ENDPOINT,
    STATUS_NOT_FOUND,
    STATUS_OK,
    TEST_DATA_DIR,
    load_json_file,
    validate_response_schema,
)


@pytest.mark.smoke
@pytest.mark.crud
@allure.title("Get list of users")
@allure.description("Fetch the paginated list of users and validate the response schema.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "get", "users")
def test_get_users_list(api_request_context: APIRequestContext, logger: logging.Logger) -> None:
    """Fetch and validate the user list response from the ReqRes API."""
    response = api_request_context.get(LIST_USERS_ENDPOINT)
    logger.info("GET %s -> %s", LIST_USERS_ENDPOINT, response.status)

    assert response.status == STATUS_OK
    payload = response.json()
    validate_response_schema(payload, "user_schema.json")


@pytest.mark.regression
@pytest.mark.crud
@allure.title("Get single user by ID")
@allure.description("Validate a single-user response payload and schema for a known valid user ID.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("api", "get", "single-user")
@pytest.mark.parametrize(
    "user_id, expected_status",
    [(2, STATUS_OK), (7, STATUS_OK)],
    ids=["user_2", "user_7"],
)
def test_get_single_user(api_request_context: APIRequestContext, logger: logging.Logger, user_id: int, expected_status: int) -> None:
    """Fetch a valid single-user response and validate the schema."""
    endpoint = SINGLE_USER_ENDPOINT.format(user_id=user_id)
    response = api_request_context.get(endpoint)
    logger.info("GET %s -> %s", endpoint, response.status)

    assert response.status == expected_status
    payload = response.json()
    validate_response_schema(payload, "user_schema.json")


@pytest.mark.regression
@pytest.mark.crud
@allure.title("Get single user with positive and negative IDs")
@allure.description("Validate both valid and invalid user ID scenarios using a shared parametrized dataset.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "get", "user-id-validation")
@pytest.mark.parametrize(
    "user_data",
    load_json_file(TEST_DATA_DIR / "negative_ids.json"),
    ids=lambda item: item["label"],
)
def test_get_single_user_parametrized(api_request_context: APIRequestContext, logger: logging.Logger, user_data: dict[str, int | str]) -> None:
    """Exercise positive and negative user ID cases using the same parametrized test."""
    endpoint = SINGLE_USER_ENDPOINT.format(user_id=user_data["id"])
    response = api_request_context.get(endpoint)
    logger.info("GET %s -> %s", endpoint, response.status)

    assert response.status == user_data["expected_status"]
    payload = response.json()

    if response.status == STATUS_OK:
        validate_response_schema(payload, "user_schema.json")
    else:
        assert isinstance(payload, dict)
        assert payload == {} or "error" in payload
