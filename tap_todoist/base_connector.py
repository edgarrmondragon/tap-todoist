from __future__ import annotations

from functools import lru_cache
from typing import Callable, Iterable, Mapping, Sequence

import requests
from singer_sdk._singerlib import Catalog, CatalogEntry

from tap_todoist.types import ConfigDict, StateDict


class HTTPConnector:
    """Base class for HTTP connectors."""

    def __init__(self):
        """Initialize the HTTPConnector class."""
        self.config = None
        self.catalog = Catalog()

    @property
    @lru_cache(maxsize=None)
    def requests_session(self) -> requests.Session:
        """Get the (cached) requests session for the connector.

        Returns:
            The requests session for the connector.
        """
        session = requests.Session()
        return session

    def get_headers(
        self,
        config: ConfigDict,
        catalog: Catalog,
        state: StateDict,
    ) -> Mapping[str, str]:
        """Get the headers for all requests.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.

        Returns:
            The headers for all requests.
        """
        return {}

    def get_query_params(
        self,
        config: ConfigDict,
        catalog: Catalog,
        state: StateDict,
    ) -> Mapping[str, str, Sequence[str]]:
        """Get the query parameters for all requests.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.

        Returns:
            The query parameters for all requests.
        """
        return {}

    def get_data(
        self,
        config: ConfigDict,
        catalog: Catalog,
        state: StateDict,
    ) -> Mapping[str, str]:
        """Get the data for all requests.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.

        Returns:
            The data for all requests.
        """
        return {}

    def get_auth(
        self,
        config: ConfigDict,
        catalog: Catalog,
        state: StateDict,
    ) -> Callable[[], requests.PreparedRequest]:
        """Get the authentication callable for all requests.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.

        Returns:
            The authentication callable for all requests.
        """
        return None

    def prepare_session(
        self,
        config=ConfigDict,
        catalog=Catalog,
        state=StateDict,
    ):
        """Prepare the requests session for the connector.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.

        Returns:
            The requests session for the connector.
        """
        self.requests_session.auth = self.get_auth(config, catalog, state)

    def send_request(self, method, url, **kwargs) -> requests.Response:
        """Send a request to the API.

        Args:
            method: The HTTP method to use.
            url: The URL to send the request to.
            **kwargs: Additional keyword arguments to pass to the request.

        Returns:
            The response from the API.
        """
        session = self.requests_session

        return session.request(
            method,
            url,
            headers=kwargs.pop("headers", None),
            params=kwargs.pop("params", None),
            data=kwargs.pop("data", None),
            **kwargs,
        )

    def discover_catalog_entries(self) -> Iterable[CatalogEntry]:
        """Discover the catalog entries for the connector.

        Returns:
            The catalog entries for the connector.
        """
        raise NotImplementedError

    def discover(self, config: ConfigDict) -> Catalog:
        """Discover the catalog for the connector.

        Args:
            config: The configuration for the connector.

        Returns:
            The catalog for the connector.
        """
        for entry in self.discover_catalog_entries():
            entry.metadata.root.selected = True
            self.catalog[entry.tap_stream_id] = entry
        return self.catalog

    def prepare(
        self,
        config: ConfigDict | None = None,
        catalog: Catalog | None = None,
        state: StateDict | None = None,
    ) -> None:
        """Prepare the connector for use.

        Args:
            config: The configuration for the connector.
            catalog: The catalog for the connector.
            state: The state for the connector.
        """
        self.prepare_session(config, catalog, state)
