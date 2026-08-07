"""Factory for creating the shared Playwright API request context.

This module exposes a single factory function that returns a Playwright
APIRequestContext configured with the project base URL and x-api-key header.
The context is then reused across the suite via pytest fixtures instead of being
created in individual test modules.
"""

from __future__ import annotations

from typing import Tuple

from playwright.sync_api import APIRequestContext, Playwright, sync_playwright

from config.environments import API_KEY, BASE_URL


def create_api_request_context() -> Tuple[APIRequestContext, Playwright]:
    """Create and return a configured Playwright API request context.

    Returns:
        A tuple containing the API request context and the Playwright instance that owns it.
    """
    base_url = BASE_URL.removesuffix("/api") if BASE_URL.endswith("/api") else BASE_URL

    playwright = sync_playwright().start()
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"x-api-key": API_KEY},
    )
    return request_context, playwright
