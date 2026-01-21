import os
import sys
import pytest

# Ensure project root is on sys.path so `src` package is importable when running pytest
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.drivers.driver import BaseDriver


@pytest.fixture(scope="function")
def driver():
    d = BaseDriver()
    try:
        yield d.driver
    finally:
        try:
            if getattr(d, "driver", None):
                try:
                    d.driver.terminate_app("com.castalk.app.uat")
                except Exception:
                    pass
        except Exception:
            pass
        d.quit()
