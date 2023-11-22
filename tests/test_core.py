"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_tap_test_class

from tap_aircall.tap import TapAircall

SAMPLE_CONFIG = {
    "start_date": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "api_key": os.getenv('TAP_AIRCALL_API_KEY'),
    "api_token": os.getenv('TAP_AIRCALL_API_TOKEN')
}


# Run standard built-in tap tests from the SDK:
TestTapAircall = get_tap_test_class(
    tap_class=TapAircall,
    config=SAMPLE_CONFIG,
)