from __future__ import annotations

import json
import logging
from typing import Iterable

import requests
import requests_cache
from singer_sdk._singerlib import Catalog, CatalogEntry, MetadataMapping
from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.streams.core import REPLICATION_LOG_BASED

from tap_todoist.base_connector import HTTPConnector
from tap_todoist.catalog import SCHEMAS
from tap_todoist.types import ConfigDict, StateDict, RequestsAuth

requests_cache.install_cache("tap_todoist_cache", backend="sqlite", expire_after=3600)


class BearerAuth(requests.auth.AuthBase):
    """Bearer Auth class for requests."""

    def __init__(self, token: str):
        """Initialize the BearerAuth class.

        Args:
            token: The token to use for authentication.
        """
        self.token = token

    def __call__(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        """Add the token to the outgoing request.

        Args:
            request: The outgoing request.

        Returns:
            The outgoing request with the token added.
        """
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


class TodoistClient(HTTPConnector):
    """Todoist API client."""

    def __init__(self):
        """Initialize the TodoistClient class."""
        super().__init__()
        self._data: dict | None = None

    def get_auth(
        self,
        config: ConfigDict,
        catalog: Catalog,
        state: StateDict,
    ) -> RequestsAuth:
        """Get the authentication callable for all requests.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.
        """
        return BearerAuth(config["token"])

    def get_data(self, config: dict, catalog: Catalog, state: dict) -> dict:
        """Get the data to send with the request.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.
        """
        selected_streams: list[str] = []
        for entry in catalog.streams:
            mask = entry.metadata.resolve_selection()
            if mask[()]:
                selected_streams.append(entry.tap_stream_id)

        return {
            "sync_token": "*",
            "resource_types": json.dumps(selected_streams),
        }

    @property
    def data(self) -> dict:
        """Get the todoist sync data.

        Returns:
            The todoist sync data.
        """
        return self._data

    def prepare(
        self,
        config: ConfigDict = None,
        catalog: Catalog = None,
        state: StateDict = None,
    ):
        super().prepare(config, catalog, state)

        response = self.send_request(
            "POST",
            "https://api.todoist.com/sync/v9/sync",
            data=self.get_data(config, catalog, state),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        self._data = response.json()
        logging.info("Full sync %s", self._data["full_sync"])
        logging.info("Sync token: %s", self._data["sync_token"])

    def discover_catalog_entries(
        self,
        config: ConfigDict = None,
    ) -> Iterable[CatalogEntry]:
        """Discover the catalog entries for the connector.

        Args:
            config: The configuration for the connector.

        Returns:
            The catalog entries for the connector.
        """
        for key in SCHEMAS:
            yield CatalogEntry(
                tap_stream_id=key,
                metadata=MetadataMapping.get_standard_metadata(
                    schema=SCHEMAS[key].to_dict(),
                    replication_method=REPLICATION_LOG_BASED,
                    key_properties=["id"],
                    valid_replication_keys=None,
                ),
                schema=SCHEMAS[key].to_schema(),
                key_properties=["id"],
            )


class SyncStream(Stream):
    """A stream for the Todoist sync API."""


    def __init__(self, tap, schema: dict, name: str, connector: TodoistClient):
        """Initialize the SyncStream class.

        Args:
            tap: The tap for the stream.
            schema: The schema for the stream.
            name: The name of the stream.
            connector: The connector for the stream.
        """
        self.connector = connector
        super().__init__(tap, schema=schema, name=name)

    def get_records(self, context: dict) -> list:
        """Get the records for the stream.

        Args:
            context: The context for the stream.

        Returns:
            The records for the stream.
        """
        return self.connector.data[self.name]


class TapTodoist(Tap):
    """Singer tap for Todoist."""

    name = "tap-todoist"
    config_jsonschema = th.PropertiesList(
        th.Property(
            "token",
            th.StringType,
            description="API token for the todoist API",
            required=True,
        ),
    ).to_dict()

    def __init__(
        self,
        config,
        catalog,
        state,
        parse_env_config=True,
        validate_config=True,
    ):
        """Initialize the TapTodoist class.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.
            parse_env_config: Whether to parse environment variables for the
                configuration.
            validate_config: Whether to validate the configuration.
        """
        self.client = TodoistClient()
        super().__init__(
            config,
            catalog,
            state,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )

        self.client.config = self.config

    @property
    def _singer_catalog(self) -> Catalog:
        return self.client.discover(self.config)

    def discover_streams(self):
        """Discover the streams for the connector.

        Returns:
            The streams for the connector.
        """
        return [
            SyncStream(
                self,
                entry["schema"],
                entry["tap_stream_id"],
                self.client,
            )
            for entry in self.catalog_dict["streams"]
        ]

    def sync_all(self) -> None:
        """Sync all streams."""
        self.client.discover(self.config)
        self.client.prepare(
            self.config,
            self.catalog or self.client.catalog,
            self.state,
        )
        return super().sync_all()
