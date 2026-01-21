from typing import Optional

from appium.webdriver.common.appiumby import AppiumBy


def clear_inputs(driver, class_name: str = "android.widget.EditText"):
    try:
        for e in driver.find_elements(AppiumBy.CLASS_NAME, class_name):
            try:
                e.clear()
                try:
                    e.set_value("")
                except Exception:
                    pass
            except Exception:
                pass
    except Exception:
        pass


def attr_enabled(el) -> bool:
    try:
        a = el.get_attribute("enabled")
        if a is not None:
            return a in ("true", "True", "1")
    except Exception:
        pass
    try:
        return el.is_enabled()
    except Exception:
        return False


def find_clickable_container_for_text(driver, text: str = "Sign In") -> Optional[object]:
    """Find a clickable container that contains an element with given text.

    Strategy: locate the Text element, compute its center, then find a clickable
    whose bounds contain that center. Fallback to clickable that has descendant
    with exact text.
    """
    try:
        sign_el = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
    except Exception:
        return None

    center_x = center_y = None
    try:
        r = sign_el.rect
        center_x = r.get('x', 0) + r.get('width', 0) / 2
        center_y = r.get('y', 0) + r.get('height', 0) / 2
    except Exception:
        pass

    try:
        clickables = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().clickable(true)')
    except Exception:
        clickables = []

    if center_x is not None and center_y is not None:
        for c in clickables:
            try:
                rr = c.rect
                x, y, w, h = rr.get('x', 0), rr.get('y', 0), rr.get('width', 0), rr.get('height', 0)
                if x <= center_x <= x + w and y <= center_y <= y + h:
                    return c
            except Exception:
                continue

    # fallback: clickable that has descendant with text
    for c in clickables:
        try:
            if c.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'):
                return c
        except Exception:
            continue

    return None


def simulate_fingerprint(driver, adb_fallback: bool = True) -> bool:
    """Try to simulate a fingerprint on the connected emulator/device.

    Returns True if a simulation command was executed, False otherwise.
    Attempts Appium `finger_print` first, then an `adb emu finger touch 1` fallback.
    """
    try:
        # Appium emulator API
        driver.finger_print(1)
        return True
    except Exception:
        if not adb_fallback:
            return False
    try:
        import subprocess
        out = subprocess.check_output(["adb", "devices"]).decode()
        lines = [l for l in out.splitlines()[1:] if l.strip()]
        if not lines:
            return False
        dev = lines[0].split()[0]
        subprocess.check_call(["adb", "-s", dev, "emu", "finger", "touch", "1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False
