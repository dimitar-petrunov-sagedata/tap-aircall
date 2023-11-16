"""Stream type classes for tap-aircall."""

from __future__ import annotations

import typing as t
import requests
from pathlib import Path
from typing import Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.typing import IntegerType, StringType, DateTimeType, ObjectType, Property, PropertiesList, ArrayType, BooleanType

from tap_aircall.client import AircallStream


class CallsStream(AircallStream):
    name = "calls"
    path = "/calls"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = 'started_at'
    is_sorted = True
    records_jsonpath = "$.calls[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("started_at", IntegerType),
        Property("answered_at", IntegerType),
        Property("ended_at", IntegerType),
        Property("duration", IntegerType),
        Property("status", StringType),
        Property("direction", StringType),
        Property("archived", BooleanType),
        Property("missed_call_reason", StringType),
        Property("cost", StringType),
        Property("number", ObjectType(Property("id", IntegerType))),
        Property("user", ObjectType(Property("id", IntegerType))),
        Property("contact", ObjectType(Property("id", IntegerType))),
        Property("assigned_to", ObjectType(Property("id", IntegerType))),
        Property("transferred_by", ObjectType(Property("id", IntegerType))),
        Property("transferred_to", ObjectType(Property("id", IntegerType))),
        Property("tags", ArrayType(ObjectType(Property("id", IntegerType))))
    ).to_dict()
    
class UsersStream(AircallStream):
    name = "users"
    path = "/users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.users[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("name", StringType),
        Property("email", StringType),
        Property("created_at", DateTimeType),
        Property("available", BooleanType),
        Property("availability_status", StringType),
        Property("numbers", ArrayType(ObjectType(Property("id", IntegerType)))),
        Property("time_zone", StringType),
        Property("language", StringType),
        Property("wrap_up_time", IntegerType)
    ).to_dict()
    
class NumbersStream(AircallStream):
    name = "numbers"
    path = "/numbers"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.numbers[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("name", StringType),
        Property("digits", StringType),
        Property("created_at", DateTimeType),
        Property("country", StringType),
        Property("time_zone", StringType),
        Property("open", BooleanType),
        Property("availability_status", StringType),
        Property("is_ivr", BooleanType),
        Property("priority", IntegerType)        
    ).to_dict()
    
class ContactsStream(AircallStream):
    name = "contacts"
    path = "/contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.contacts[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("first_name", StringType),
        Property("last_name", StringType),
        Property("company_name", StringType),
        Property("description", StringType),
        Property("information", StringType),
        Property("is_shared", BooleanType)     
    ).to_dict()
    
class TagsStream(AircallStream):
    name = "tags"
    path = "/tags"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.tags[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("name", StringType),
        Property("color", StringType),
        Property("description", StringType) 
    ).to_dict()