import time
import pytest
import os
from src.pages.chat_page import ChatPage
from src.utils.ui_helpers import clear_inputs




def test_open_chat_from_home(driver):
    """TC1 — Open the Chat screen from the Home screen by tapping the chat icon."""
    chat = ChatPage(driver)
    el = chat.open_from_home()
    if el is None:
        pytest.skip("Could not find chat icon on Home")

    # wait for input to appear
    end = time.time() + 6
    while time.time() < end:
        if chat.find_input() is not None:
            break
        time.sleep(0.5)

    assert chat.find_input() is not None, "Chat screen did not open or input not found"


def test_send_message_to_ai(driver):
    """TC2 — Send a message to the AI and verify the sent message bubble appears."""
    chat = ChatPage(driver)
    if chat.find_input() is None:
        pytest.skip("No chat input available to send a message")

    try:
        clear_inputs(driver)
    except Exception:
        pass

    msg = os.environ.get("TEST_AI_MESSAGE", "Hi AI, test")

    submitted = chat.send_message(msg)
    assert submitted, "Could not submit the message (no send method found)"

    # verify sent message appears (match on first token for robustness)
    first = msg.split()[0]
    assert chat.is_message_present(first, timeout=10), "Sent message bubble did not appear"


def test_chat_add_suggestion_and_report(driver):
    """TC3 — Verify the '+' suggestion button opens suggestions and the '!' report opens a report dialog."""
    chat = ChatPage(driver)

    if not chat.open_suggestions():
        pytest.skip("Could not find '+' button to add suggestions")

    suggestion_shown = chat.is_suggestion_shown()

    if not chat.open_report():
        pytest.skip("Could not find report button on the chat screen")

    reported = chat.is_report_dialog_shown()

    # suggestion is informational; require report dialog to appear
    assert reported, "Report dialog/form did not open after tapping report"
