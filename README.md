# Pytest Token Auth Example

This repository shows how to write API tests in Python using several approaches and good practices. It focuses on:
- Token-based authentication and session management
- A small API client layer on top of requests
- Response models and validation with Pydantic (DTOs)
- Soft assertions to collect multiple failures in one test
- Clean pytest configuration, fixtures, and Allure reporting

The tests are implemented for https://github.com/crowin/marketplace-spring-microservices (written by me)

## Key Features and Approaches

- Token auth with session cache
  - A login request gets a bearer token at the start of the test session.
  - The token is stored as a local file in a temporary folder and reused in tests.
  - Works with pytest-xdist: all workers read the same token file, so one token is shared across parallel workers.
  - The folder is removed after the test session finishes.

- API client layer
  - `core/api/market_client.py` wraps HTTP calls with `requests.Session`.
  - Authorization headers are attached once during client creation.

- DTOs with Pydantic
  - `core/api/market/market_dto.py` defines response models (`Product`, `Cart`, `CartDto`).
  - Models use field constraints and alias generation (camelCase) to match API payloads and validate data.

- Soft assertions
  - `tests/soft_assertion.py` collects multiple assertion errors before failing the test.
  - Useful for validating many similar conditions (for example, every cart has products).

- Pytest fixtures and hooks
  - `tests/conftest.py` prepares auth sessions in `pytest_configure` and removes them in `pytest_sessionfinish`.
  - `basic_user_api` fixture exposes a ready-to-use `CartsApi` client for tests.

- Allure reporting
  - Allure steps (`@allure.step`) and titles are used across clients and tests.

## Part of Project Structure

- `core/`
  - `api/user/auth_client.py` — login and local token session helpers
  - `api/market/market_client.py` — Carts API client (GET carts, get by id, get by user id)
  - `api/market/market_dto.py.py` — Pydantic response models (DTOs)
  - `api/user.py` — simple `User` entity that reads token from local session
  - `config.py` — builds URLs and folder names from environment variables
- `tests/`
  - `conftest.py` — session init/cleanup, fixtures
  - `api_assertions.py` — basic response status assertions
  - `soft_assertion.py` — soft assertion helper
  - `market/test_products_api.py` — example tests for carts endpoints
  - `test_user.py` — test users built from environment
- `.env` — environment variables used by pytest/Code under test
- `pytest.ini` — pytest configuration (env file, warnings, addopts)
- `requirements.txt` — dependencies

## Requirements

- Python 3.10+ (recommended)
- pip

## Installation

1. Clone the repository.
2. Create and activate a virtual environment (optional but recommended):
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate`
   - Windows (PowerShell): `py -m venv .venv; .\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   - `pip install -r requirements.txt`

## Environment Configuration

The project uses `pytest-dotenv` to load variables from the `.env` file in the repository root. Default values are already provided for the dummy API:

You can adjust these values if needed. The `USER_SESSIONS_DIR` is created automatically for token files and removed after the test session.

## How Authentication Works Here

- On session start, `conftest.py` logs in each configured user and writes a token file to `USER_SESSIONS_DIR`.
- The `User` object reads the token from that file when creating API clients.
- Requests include `Authorization: Bearer <token>` header.

Note: For the dummy API, these tokens are examples used for demonstration only.

### Parallel runs and token sharing

- The token is written once per user into a shared folder (`USER_SESSIONS_DIR`). When you run tests with `pytest -n <workers>`, every xdist worker process reads the same token file. As a result, a single token is reused across all workers, avoiding extra login calls and making parallel runs stable and fast.
- Cleanup is performed only by the main process at session end. In `tests/conftest.py`, `pytest_sessionfinish` checks that it is not a worker (no `workerinput`) before removing the folder. This ensures workers do not race to delete the tokens.
- Initialization also avoids duplication: `_init_all_sessions()` creates a token file only if it does not exist, so concurrent workers typically reuse the already-created file. If you expect heavy contention, consider adding a simple file lock around token creation.
- If you prefer a unique token per worker, you can change the session file naming scheme to include the worker id (e.g., `f"{username}_{workerid}_token.json"`) and set `Authorization` accordingly.

## Running Tests

- Run all tests:
  - `pytest`

- Run tests in parallel (example: 4 workers):
  - `pytest -n 4`

- Run a specific test file:
  - `pytest tests/dump_service/test_products_api.py`

- Run a single test by name:
  - `pytest tests/dump_service/test_products_api.py::test_get_carts`

## Allure Reports

Allure is integrated at test and client levels via steps and titles.

- Generate raw results:
  - `pytest --alluredir=allure-results`

- View the report (requires the Allure commandline to be installed):
  - `allure serve allure-results`

If you do not have the CLI, install it following the official Allure instructions for your OS.

## Example Test Flow

Example from `tests/dump_service/test_products_api.py`:
- Get all carts with `basic_user_api.get_cart()`.
- Assert the HTTP status is OK.
- Parse and validate the response into `CartDto`.
- Use `SoftAssert` to ensure every cart has at least one product.

## Notes and Good Practices Shown

- Separate layers: configuration, API clients, models, tests.
- Clear boundaries between data (DTOs) and transport (requests Session).
- Reusable fixtures for test stability and readability.
- Soft assertions for broader coverage per test run.
- Environment-driven configuration for portability.

## Troubleshooting

- If tokens are not created: check `.env` values and network access.
- If imports fail: ensure `pytest.ini` sets `pythonpath = ["core",]` and you run pytest from the project root.
- If Allure report does not open: make sure the Allure commandline is installed and available in PATH.

## License

This project is intended for educational and demonstration purposes.
