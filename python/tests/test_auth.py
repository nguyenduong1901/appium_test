import os
import os
import pytest
from src.pages.auth_page import AuthPage


def test_login_success(driver):
    """TC1 — Successful login (Email/Password) using `AuthPage` page object."""

    email = os.environ.get("TEST_EMAIL", "user@castalk.com")
    password = os.environ.get("TEST_PASSWORD", "Password123")

    auth = AuthPage(driver)
    auth.open_email_signin()
    auth.fill_credentials(email, password)
    auth.submit()

    # verify sign-in affordance disappeared or a post-login element is visible
    assert not auth.is_signin_affordance_present(timeout=10) or auth.is_logged_in(), "Login may have failed"


def test_login_invalid_password(driver):
    """TC2 — Failed login (incorrect password)."""
    email = os.environ.get("TEST_EMAIL", "user@castalk.com")
    wrong = os.environ.get("TEST_WRONG_PASSWORD", "WrongPass123")

    auth = AuthPage(driver)
    auth.open_email_signin()
    auth.fill_credentials(email, wrong)
    auth.submit()

    # Expect the specific error message shown in the app UI
    expected_msg = "Incorrect email address or password. Please try again."
    assert auth.expect_error(expected_msg), f"Expected error message not found: {expected_msg}"


def test_login_empty_fields_validation(driver):
    """TC3 — Validation for empty email/password.

    Expectation: when either field empty, `Sign In` button is disabled; when both filled, enabled.
    """
    from appium.webdriver.common.appiumby import AppiumBy
    import time
    from src.utils.ui_helpers import clear_inputs, find_clickable_container_for_text, attr_enabled

    auth = AuthPage(driver)
    auth.open_email_signin()

    clear_inputs(auth.driver)
    time.sleep(0.5)

    container = find_clickable_container_for_text(auth.driver, "Sign In")
    if container is None:
        pytest.fail("Could not find clickable container for 'Sign In'")

    assert not attr_enabled(container), "Sign In should be disabled when fields are empty"

    auth.fill_credentials(os.environ.get("TEST_EMAIL", "user@castalk.com"), os.environ.get("TEST_PASSWORD", "Password123"))
    end = time.time() + 5
    while time.time() < end:
        if attr_enabled(container):
            break
        time.sleep(0.5)

    assert attr_enabled(container), "Sign In should be enabled when email and password are provided"


def test_biometric_login(driver):
    """TC4 — Biometric login (emulator friendly)."""
    from src.utils.ui_helpers import simulate_fingerprint
    import time

    auth = AuthPage(driver)
    if not auth.click_biometric():
        pytest.skip("No biometrics Set Up")

    # small wait for modal to appear if any
    time.sleep(0.5)
    if auth.expect_error("No Biometrics", timeout=1):
        pytest.skip("Biometrics not enabled in app")

    if not simulate_fingerprint(auth.driver):
        pytest.skip("Cannot simulate fingerprint in this environment")

    assert auth.is_logged_in(), "Biometric login did not result in logged-in state"


def test_google_oauth_flow_starts(driver):
    """TC5 — Clicking Google login starts OAuth (detect WEBVIEW or account chooser)."""
    auth = AuthPage(driver)
    if not auth.click_google():
        pytest.skip("Google login button not present")

    import time
    end = time.time() + 6
    while time.time() < end:
        try:
            contexts = auth.driver.contexts
        except Exception:
            contexts = []

        if any("WEBVIEW" in (c or "") for c in contexts):
            break

        if auth.expect_error(timeout=1) or not auth.is_signin_affordance_present(timeout=1):
            break

        time.sleep(0.5)

    else:
        pytest.fail("OAuth flow did not start (no WEBVIEW/context change)")

    try:
        auth.driver.back()
    except Exception:
        pass


    

