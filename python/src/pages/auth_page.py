from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from typing import Optional
import time


class AuthPage(BasePage):
    """Page object for Castalk auth screens.

    Provides resilient selectors and high-level actions used across tests.
    """

    def open_email_signin(self):
        # Try quick non-blocking checks first to avoid long waits when items aren't present
        try:
            els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Sign in with email")')
            if els:
                els[0].click()
                return els[0]
        except Exception:
            pass

        try:
            els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Sign In")')
            if els:
                els[0].click()
                return els[0]
        except Exception:
            pass

        # Fallback to waiting click for cases where element may appear after scrolling
        return self.click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Sign In")')

    def fill_credentials(self, email: str, password: str):
        # Prefer finding two EditText fields; else try placeholders
        els = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(els) >= 2:
            els[0].clear(); els[0].send_keys(email)
            els[1].clear(); els[1].send_keys(password)
            return

        # fallback by placeholder text seen in screenshots
        try:
            self.send_keys(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Enter Your Email")', email)
        except Exception:
            pass
        try:
            self.send_keys(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Enter Your Password")', password)
        except Exception:
            pass

    def submit(self):
        # click bottom 'Sign In' if present, else click first clickable with 'Sign'
        # quick non-blocking attempt
        try:
            els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
            if els:
                els[0].click()
                return els[0]
        except Exception:
            pass

        try:
            els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().clickable(true)')
            for e in els:
                txt = ''
                try:
                    txt = e.text or ''
                except Exception:
                    pass
                if 'sign' in txt.lower():
                    e.click()
                    return
            if els:
                els[0].click()
                return els[0]
        except Exception:
            pass

        # fallback to waiting click if nothing found quickly
        try:
            return self.click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Sign In")')
        except Exception:
            return None

    def is_signin_affordance_present(self, timeout: int = 3) -> bool:
        try:
            return bool(self.wait.until(lambda d: d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Sign in with email")')))
        except Exception:
            return False

    def is_logged_in(self, timeout: int = 5) -> bool:
        # best-effort: check for a known post-login element (app-specific)
        # Consumers may override or update this selector as app evolves.
        try:
            return bool(self.wait.until(lambda d: d.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("home")')))
        except Exception:
            return False

    def expect_error(self, text: Optional[str] = None, timeout: int = 5) -> bool:
        """Wait up to `timeout` seconds for an error message.

        If `text` provided, look for that substring; else check common keywords.
        """
        keywords = [text] if text else ["incorrect", "invalid", "error", "please enter", "required"]
        end = time.time() + timeout
        while time.time() < end:
            for kw in keywords:
                if not kw:
                    continue
                ua = f'new UiSelector().textContains("{kw}")'
                try:
                    els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, ua)
                    if els:
                        return True
                except Exception:
                    continue
            time.sleep(0.5)
        return False

    def click_biometric(self):
        """Try to click biometric affordance (fingerprint icon).

        Returns True if clicked, False otherwise.
        """
        # common descriptors: fingerprint, biometric, touch
        candidates = [
            'new UiSelector().descriptionContains("finger")',
            'new UiSelector().descriptionContains("biometric")',
            'new UiSelector().textContains("finger")',
            'new UiSelector().textContains("biometric")',
        ]
        for ua in candidates:
            try:
                els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, ua)
                if els:
                    els[0].click()
                    return True
            except Exception:
                continue
        return False

    def click_google(self) -> bool:
        """Click 'Continue with Google' button if present."""
        try:
            self.click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Continue with Google")')
            return True
        except Exception:
            # try by package or partial text
            try:
                self.click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Google")')
                return True
            except Exception:
                return False
