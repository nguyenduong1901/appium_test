from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple, Any


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 8):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, by: By, locator: str):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by: By, locator: str):
        el = self.find(by, locator)
        el.click()
        return el

    def send_keys(self, by: By, locator: str, text: str):
        el = self.find(by, locator)
        el.clear()
        el.send_keys(text)
        return el

    def find_one_of(self, selectors: list[Tuple[By, str]]):
        """Try a list of selectors and return the first that matches.

        selectors: list of tuples like (AppiumBy.ID, "id") or (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector()...')
        """
        last_ex = None
        for by, locator in selectors:
            try:
                return self.find(by, locator)
            except Exception as ex:
                last_ex = ex
                continue
        # re-raise the last exception for visibility
        if last_ex:
            raise last_ex
        raise Exception("No selectors provided")

    def find_by_text_contains(self, text: str):
        ua = f'new UiSelector().textContains("{text}")'
        return self.find(AppiumBy.ANDROID_UIAUTOMATOR, ua)

    def find_by_desc_contains(self, desc: str):
        ua = f'new UiSelector().descriptionContains("{desc}")'
        return self.find(AppiumBy.ANDROID_UIAUTOMATOR, ua)

    def scroll_into_view_by_text(self, text: str):
        # Uses UiScrollable to scroll until element with textContains is visible
        ui = (
            'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView('
            f'new UiSelector().textContains("{text}"));'
        )
        return self.find(AppiumBy.ANDROID_UIAUTOMATOR, ui)

    def wait_for(self, by: By, locator: str, timeout: int = None):
        wt = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wt.until(EC.presence_of_element_located((by, locator)))

