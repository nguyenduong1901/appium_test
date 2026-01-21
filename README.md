# Appium Mobile Testing Framework

A comprehensive test automation framework for mobile applications using Appium, Python, and Pytest. This project implements best practices for mobile application testing using the Page Object Model design pattern.

## Overview

This repository contains an automated testing suite for mobile applications, specifically designed for Android testing using Appium. The framework is built with the following technologies:

- **Appium 3.1.2** - Mobile test automation framework
- **Python 3.13** - Programming language
- **Pytest** - Test framework
- **Selenium** - WebDriver for Appium
- **Page Object Model** - Design pattern for test organization

## Key Features

- Page Object Model (POM) architecture for maintainability and scalability
- Multiple test scenarios for authentication flows and user interactions
- Support for biometric login testing
- OAuth integration testing capabilities
- Form validation testing
- Reusable UI helpers and utility functions
- Configuration management for different environments
- Android Debug Bridge (ADB) integration

## Project Structure

```
appium/
├── python/                          # Main test project
│   ├── config/
│   │   └── dev_caps.json           # Device capabilities configuration
│   ├── src/
│   │   ├── drivers/
│   │   │   └── driver.py           # Appium driver initialization
│   │   ├── pages/
│   │   │   ├── base_page.py        # Base page object class
│   │   │   ├── auth_page.py        # Authentication page object
│   │   │   └── chat_page.py        # Chat page object
│   │   └── utils/
│   │       ├── config.py           # Configuration utilities
│   │       ├── adb.py              # ADB utilities
│   │       └── ui_helpers.py       # UI interaction helpers
│   ├── tests/
│   │   ├── conftest.py             # Pytest fixtures
│   │   ├── test_auth.py            # Authentication tests
│   │   └── test_chat_ai.py         # Chat/AI tests
│   ├── requirements.txt            # Python dependencies
│   ├── pytest.ini                  # Pytest configuration
│   └── README.md                   # Python project documentation
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Getting Started

### System Requirements

- Python 3.13+
- Node.js (for Appium)
- Android SDK (for adb and emulator)
- Git

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/nguyenduong1901/appium_test.git
   cd appium_test
   ```

2. Create and activate virtual environment:
   ```bash
   cd python
   python -m venv .venv
   
   # On Windows
   .\.venv\Scripts\Activate.ps1
   
   # On Linux/Mac
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Appium server:
   ```bash
   npm install -g appium
   appium driver install uiautomator2
   ```

## Configuration

### Device Capabilities Configuration

Edit the device capabilities file `python/config/dev_caps.json` to configure your Android device:

```json
{
  "platformName": "Android",
  "appium:deviceName": "emulator-5554",
  "appium:automationName": "UiAutomator2",
  "appium:appPackage": "com.example.app",
  "appium:appActivity": ".MainActivity"
}
```

### Environment Variables

Set these environment variables before running tests:

```bash
export TEST_EMAIL="test@example.com"
export TEST_PASSWORD="Password123"
export TEST_WRONG_PASSWORD="WrongPass123"
```

## Running Tests

### Starting the Appium Server

```bash
appium
```

### Running All Tests

```bash
cd python
pytest tests/ -v
```

### Running a Specific Test

```bash
pytest tests/test_auth.py::test_login_success -v
```

### Running Tests with Code Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Running Tests in Parallel

```bash
pytest tests/ -n auto
```

## Test Cases

### Authentication Test Suite (test_auth.py)

1. test_login_success: Validates successful login with correct credentials
2. test_login_invalid_password: Tests error handling for incorrect password
3. test_login_empty_fields_validation: Verifies form validation rules
4. test_biometric_login: Tests biometric authentication flow
5. test_google_oauth_flow_starts: Validates OAuth integration initiation

## Architecture and Design Patterns

### Page Object Model Implementation

The framework implements the Page Object Model (POM) design pattern for better code organization and maintainability:

```python
# Example usage
from src.pages.auth_page import AuthPage

def test_login(driver):
    auth = AuthPage(driver)
    auth.open_email_signin()
    auth.fill_credentials("user@example.com", "Password123")
    auth.submit()
    assert auth.is_logged_in()
```

## Utilities and Helper Functions

### UI Helpers Module (src/utils/ui_helpers.py)

- find_element(): Locate elements with retry logic
- click_element(): Click operations with wait mechanisms
- send_keys(): Type text with wait conditions
- wait_for_element(): Explicit wait wrapper
- simulate_fingerprint(): Biometric simulation

### ADB Utilities Module (src/utils/adb.py)

- Device connection management
- Screenshot capture functionality
- Application installation and uninstallation
- Device logs retrieval

### Configuration Utilities (src/utils/config.py)

- Device capabilities loading
- Environment variable management

## Development Best Practices

1. Page Object Model: Separate UI interactions from test logic
2. Wait Strategies: Use explicit waits instead of hardcoded delays
3. Test Data: Store sensitive data in environment variables
4. Logging: Implement comprehensive logging for debugging
5. Error Handling: Provide graceful error messages and recovery
6. Fixtures: Utilize Pytest fixtures for setup and teardown operations

## Continuous Integration and Deployment

### GitHub Actions Integration Example

Create `.github/workflows/test.yml` for automated test execution:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - run: pip install -r python/requirements.txt
      - run: cd python && pytest tests/ -v
```

## Troubleshooting

### Connection Refused Error
Error: [WinError 10061] No connection could be made because the target machine actively refused it
```

**Resolution:** Ensure the Appium server is running on port 4723

### Device Not Found Error
```
Error: No connected devices found
```

**Resolution:**
- Verify emulator or device is running: `adb devices`
- Confirm device name matches the configuration in `dev_caps.json`

### Appium Driver Not Found Error
```
Error: AndroidUiautomator2Driver not found
```

**Resolution:** Install the required driver
```bash
appium driver install uiautomator2
```

## References and Documentation

- [Appium Official Documentation](http://appium.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Selenium WebDriver Documentation](https://selenium.dev/)

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -m 'Add YourFeature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a Pull Request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact Information

**Author:** Nguyen Duong

- GitHub: [nguyenduong1901](https://github.com/nguyenduong1901)
- Email: nguyenduong1901@example.com

For questions, issues, or feature requests, please open an issue on GitHub.

---

Last Updated: January 22, 2026
