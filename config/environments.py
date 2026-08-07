"""Environment configuration for the ReqRes API test suite.

This module centralizes the base URL and API key configuration and loads values from
environment variables via python-dotenv. Defaults are provided so the suite still works
without a local .env file while keeping the credentials out of the test code.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

BASE_URL: str = os.getenv("REQRES_BASE_URL", "https://reqres.in/api")
API_KEY: str = os.getenv("REQRES_API_KEY", "free_user_3HEGIAwcdMAzgC8cvRnQy2cPDv6")
