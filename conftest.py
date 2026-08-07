"""Shared pytest fixtures, logging, and failure hooks for the ReqRes API suite.

This module centralizes the Playwright APIRequestContext, logger configuration, and
common project paths so tests can stay focused on validation logic rather than setup
and teardown details.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pytest
from playwright.sync_api import APIRequestContext

from context.get_context import create_api_request_context

PROJECT_ROOT = Path(__file__).resolve().parent
LOGS_DIR = PROJECT_ROOT / "logs"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
VIDEOS_DIR = PROJECT_ROOT / "videos"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """Return a shared logger reused across the entire test session.

    Returns:
        A configured logger that writes to both the console and a file in logs/.
    """
    logger_instance = logging.getLogger("reqres_api")
    logger_instance.setLevel(logging.INFO)
    logger_instance.propagate = False

    if not logger_instance.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger_instance.addHandler(stream_handler)

        file_handler = logging.FileHandler(LOGS_DIR / "api_tests.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger_instance.addHandler(file_handler)

    return logger_instance


@pytest.fixture(scope="session")
def api_request_context(logger: logging.Logger) -> APIRequestContext:
    """Create and yield the shared Playwright API request context.

    Args:
        logger: Central logger used to record context lifecycle information.

    Yields:
        A single Playwright APIRequestContext reused across the test suite.
    """
    logger.info("Creating shared API request context.")
    request_context, playwright = create_api_request_context()

    try:
        yield request_context
    finally:
        logger.info("Disposing shared API request context.")
        request_context.dispose()
        playwright.stop()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[Any]) -> None:
    """Capture useful failure details for troubleshooting API test failures.

    This hook logs the test name and any response metadata that may be attached to the
    item by tests when a failure occurs. A screenshot path is also reserved under the
    project screenshots/ directory for any future UI-adjacent debug capture.

    Args:
        item: The test item being executed.
        call: The test call result.
    """
    if call.when == "call" and call.excinfo is not None:
        logger = logging.getLogger("reqres_api")
        logger.error("Test failed: %s", item.nodeid)

        artifact = {
            "test": item.nodeid,
            "status": "failed",
            "message": str(call.excinfo.value),
            "screenshots_dir": str(SCREENSHOTS_DIR),
            "videos_dir": str(VIDEOS_DIR),
        }

        artifact_path = SCREENSHOTS_DIR / f"{item.name}_failure.json"
        artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
        logger.error("Failure artifact saved to %s", artifact_path)
