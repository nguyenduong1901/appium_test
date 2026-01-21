# Appium Python Automation (Mẫu)

# Appium Python Automation (Example)

This repository contains a minimal Appium + pytest example for automating Android app flows.

Quick start (macOS / Linux):

1) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies

```bash
python -m pip install -r requirements.txt
```

3) Start Appium server (or Appium Desktop)

```bash
# if Appium is installed globally
appium --port 4723
# or with npx if not installed globally
npx appium --port 4723
```

4) Verify device / emulator

```bash
adb devices
```

5) Update device capabilities

Edit `config/dev_caps.json` and set appropriate values for `appPackage`, `appActivity`, `deviceName`, `platformVersion`, `noReset`, etc.

6) Run tests

- Run the full suite (includes per-test durations):

```bash
pytest -r a --durations=0 -s
```

- Run a single test:

```bash
pytest tests/test_auth.py::test_google_oauth_flow_starts -q -s
```

- Or use the helper script:

```bash
./scripts/run_tests.sh
```

7) Optional environment variables

- `TEST_EMAIL`, `TEST_PASSWORD`, `TEST_WRONG_PASSWORD` — set these to override credentials used by tests.

8) Artifacts & debugging

- Save junit/artifacts into `results/` (example): `pytest --junitxml=results/results.xml`.
- For UI debugging you can call `driver.page_source`, `driver.save_screenshot()` or use ADB to pull `uiautomator` dumps and screenshots.

Troubleshooting tips

- If an element cannot be found: ensure the app is in the foreground, `config/dev_caps.json` is correct, and inspect `adb shell dumpsys activity top`.
- If Appium fails to start: try `npx appium` or install Appium globally (`npm i -g appium`).

If you want, I can add example commands to automatically collect artifacts into `results/` or update `./scripts/run_tests.sh` for CI integration.
