from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from typing import Optional
import time


class ChatPage(BasePage):
    """Page object for the Chat screen and related actions.

    Provides resilient selectors and high-level actions used by chat tests.
    """

    def open_from_home(self) -> Optional[object]:
        """Try to open the chat screen from the app Home by tapping the chat icon.

        Returns the tapped element if successful, or None.
        """
        try:
            sel = 'new UiSelector().className("android.widget.Button").instance(2)'
            el = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, sel)
            try:
                el.click()
            except Exception:
                try:
                    self.driver.execute_script("mobile: clickGesture", {"elementId": el.id})
                except Exception:
                    pass
            return el
        except Exception:
            return None

    def find_input(self) -> Optional[object]:
        """Return the chat input element if found, else None."""
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Type Something")')
        except Exception:
            pass
        try:
            return self.driver.find_element(AppiumBy.IOS_PREDICATE, 'value CONTAINS "Type Something"')
        except Exception:
            pass
        try:
            els = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if els:
                return els[0]
        except Exception:
            pass
        return None

    def send_message(self, text: str) -> bool:
        """Enter `text` into the chat input and submit. Returns True if a submit action was attempted."""
        inp = self.find_input()
        if not inp:
            return False

        try:
            inp.click()
        except Exception:
            pass

        try:
            inp.clear()
        except Exception:
            pass

        try:
            inp.send_keys(text)
        except Exception:
            try:
                inp.set_value(text)
            except Exception:
                return False

        # try keyboard submit
        try:
            self.driver.press_keycode(66)
            return True
        except Exception:
            pass

        # fallback: try a send button
        try:
            send = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("send")')
            send.click()
            return True
        except Exception:
            pass

        return False

    def is_message_present(self, text_fragment: str, timeout: int = 8) -> bool:
        end = time.time() + timeout
        while time.time() < end:
            try:
                if self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text_fragment}")'):
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False

    def open_suggestions(self) -> bool:
        """Tap the '+' suggestion button. Returns True if clicked."""
        try:
            els = self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("+")')
            if els:
                els[0].click()
                return True
        except Exception:
            pass
        try:
            el = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "+")
            el.click()
            return True
        except Exception:
            pass
        return False

    def is_suggestion_shown(self) -> bool:
        try:
            return bool(self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Suggestion")'))
        except Exception:
            return False

    def open_report(self) -> bool:
        """Tap the report button/icon. Returns True if clicked."""
        try:
            el = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("report")')
            el.click()
            return True
        except Exception:
            pass
        try:
            el = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("!")')
            el.click()
            return True
        except Exception:
            pass
        return False

    def is_report_dialog_shown(self) -> bool:
        try:
            return bool(self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Report")') or self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Reason")'))
        except Exception:
            return False
