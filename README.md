# GitHub Copilot API Testing Demo

This project is a Playwright-powered API test automation suite built with Pytest and designed to validate ReqRes API CRUD workflows. It uses a shared `APIRequestContext`, JSON Schema validation, Allure reporting, and HTML reporting to provide a clean, maintainable structure for reliable API verification.

## Project purpose

The suite exercises the following ReqRes endpoints:
- GET list users
- GET single user
- POST create user
- PUT/PATCH update user
- DELETE user

Each response is validated with JSON Schema documents located in `utils/schemas/` instead of repeated field-by-field assertions.

## Folder structure

```text
GitHub_Copilot_API_Testing_Demo/
├── pytest.ini
├── conftest.py
├── requirements.txt
├── README.md
├── config/
│   └── environments.py
├── context/
│   └── get_context.py
├── utils/
│   ├── test_data.py
│   └── schemas/
│       ├── user_schema.json
│       ├── create_user_schema.json
│       └── update_user_schema.json
├── test_data/
│   ├── create_user_data.json
│   ├── update_user_data.json
│   └── negative_ids.json
├── tests/
│   ├── test_get_users.py
│   ├── test_create_user.py
│   ├── test_update_user.py
│   └── test_delete_user.py
├── reports/
│   ├── allure-report/
│   └── html-report/
├── screenshots/
├── videos/
├── logs/
└── .env (optional, if you want to override defaults locally)
```

## Setup

1. Create and activate a virtual environment if desired.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install the Playwright browser binaries:

```bash
playwright install
```

4. Optional: create a `.env` file in the project root to override the defaults.

Example:

```env
REQRES_BASE_URL=https://reqres.in/api
REQRES_API_KEY=free_user_3HEGIAwcdMAzgC8cvRnQy2cPDv6
```

## Running tests

Run the entire suite:

```bash
pytest
```

Run only smoke tests:

```bash
pytest -m smoke
```

Run only regression tests:

```bash
pytest -m regression
```

## Allure report

Generate the results from Pytest automatically via the configured `--alluredir` setting, then view them with the Allure CLI:

```bash
allure serve reports/allure-report
```

If Allure is not installed, install it first via the official package manager and then run the command above.

## Logs and screenshots

- Logs are written to `logs/pytest_api.log`.
- Failure artifacts are saved under `screenshots/`.
- `videos/` is reserved for future UI-hybrid or browser-assisted debugging runs even though this project is API-only.

## Notes

This suite intentionally avoids `sleep()` and hardcoded waits because API requests are synchronous at the HTTP layer and should rely on real response handling rather than timing-based retries.

<!-- CI/CD auto-trigger test -->