"""REST client handling, including AircallStream base class."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Iterable
import base64
from urllib.parse import urlencode
from datetime import datetime
from urllib.parse import parse_qsl


import requests
from requests import Response
from singer_sdk.authenticators import BasicAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BasePageNumberPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
from singer_sdk.pagination import BaseHATEOASPaginator


if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class MyPaginator(BaseHATEOASPaginator):
    def get_next_url(self, response):
        data = response.json()
        return data.get("meta").get("next_page_link")
    
# class MyPaginator(BasePageNumberPaginator):
#     def has_more(self, response: Response) -> bool:
#         return response.json().get('meta').get('next_page_link') != None

class AircallStream(RESTStream):
    """Aircall stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return "https://api.aircall.io/v1"

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @property
    def authenticator(self):
        """Return the authenticator.
        """
        return BasicAuthenticator.create_for_stream(
            self,
            username=self.config.get('api_key'),
            password=self.config.get('api_token')
        )

    def get_url_params(self, context, next_page_token):
        params = {}
        start_date = self.get_starting_replication_key_value(context)
        
        if start_date:
            if type(start_date) == str:
                start_date = int(datetime.timestamp(datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")))
            params.update({"from": start_date})
            
        if next_page_token:
            params.update(parse_qsl(next_page_token.query))
            
        return params
    
    def get_new_paginator(self) -> BaseHATEOASPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return MyPaginator()


