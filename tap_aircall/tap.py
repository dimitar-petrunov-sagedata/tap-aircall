"""Aircall tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_aircall import streams


class TapAircall(Tap):
    """Aircall tap class."""

    name = "tap-aircall"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The key to authenticate against the API service",
        ),
        th.Property(
            "api_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.AircallStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CallsStream(self),
            streams.UsersStream(self),
            streams.NumbersStream(self),
            streams.ContactsStream(self),
            streams.TagsStream(self)
        ]


if __name__ == "__main__":
    TapAircall.cli()
