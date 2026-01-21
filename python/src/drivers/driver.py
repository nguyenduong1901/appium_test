from pathlib import Path
import json
from appium import webdriver
from typing import Optional

try:
    # Appium v5+ options
    from appium.options.common import AppiumOptions
except Exception:
    AppiumOptions = None


class BaseDriver:
    """Simple Appium driver wrapper that loads capabilities from JSON."""

    def __init__(self, config_path: Optional[str] = None):
        config_file = (
            Path(config_path)
            if config_path
            else Path(__file__).resolve().parents[2] / "config" / "dev_caps.json"
        )
        with open(config_file, "r") as f:
            cfg = json.load(f)

        server_url = cfg.get("server_url", "http://localhost:4723/wd/hub")
        caps = cfg.get("caps", {})

        if AppiumOptions is not None:
            opts = AppiumOptions()
            for k, v in caps.items():
                opts.set_capability(k, v)
            self.driver = webdriver.Remote(command_executor=server_url, options=opts)
        else:
            # fallback for older clients
            self.driver = webdriver.Remote(server_url, caps)

    def quit(self):
        try:
            if getattr(self, "driver", None):
                self.driver.quit()
        except Exception:
            pass
