import aiohttp
from aiogqlc import GraphQLClient as AioGraphQLClient
import asyncio
import logging
import coloredlogs
from quartic_sdk._version import __version__
from typing import Optional, Union
from urllib.parse import urlparse
import re

SCHEMA_REGEX = re.compile(r"(?:(?:https?)://)")


class GraphqlClient:
    """
    Execute Query.
    """

    def __init__(self, url: str,
                 username: str = None,
                 password: str = None,
                 token: str = None,
                 timeout: Optional[Union[aiohttp.ClientTimeout, float]] = None,
                 verify_ssl: bool = True):
        """
        class initialisation
        :param url: Client host url. For example ( https://stag.quartic.ai/)
        :param username: Username to be used to make any query/Mutation with BasicAuth.
        :param password: Password to be used to make any query/Mutation with BasicAuth.
        :param timeout: Timeout in seconds or :class:`aiohttp.ClientTimeout` object
        :param token: Token to be used to make any any query/Mutation with Oauth2.0
        """
        if username and not password:
            raise AttributeError('Need to provide password')
        if password and not username:
            raise AttributeError('Need to provide username')
        if not password and not username and not token:
            raise AttributeError(
                'Need to provide either username and password or oauth token')
        self.url = url
        self.username = username
        self.password = password
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.__graphql_url = self._get_graphql_url()
        self.logger = logging.getLogger()
        coloredlogs.install(level='DEBUG', logger=self.logger)

    @staticmethod
    def version():
        """
        Return the SDK version
        """
        return __version__

    async def _get_client(self) -> aiohttp.ClientSession:
        """
        Get aiohttp client session object.
        """
        _client_opts = {}
        if self.username and self.password:
            _opts = {
                'login': self.username,
                'password': self.password
            }

            _client_opts['auth'] = aiohttp.BasicAuth(**_opts)
        elif self.token:
            _client_opts['headers'] = {'Authorization': f"Bearer {self.token}"}
        else:
            raise AttributeError('Authentication method not found')

        if self.timeout:
            if isinstance(self.timeout, aiohttp.ClientTimeout):
                _client_opts.update(timeout=self.timeout)
            else:
                _client_opts.update(
                    timeout=aiohttp.ClientTimeout(total=self.timeout))
        _client_opts['connector'] = aiohttp.TCPConnector(ssl=self.verify_ssl)
        return aiohttp.ClientSession(**_client_opts)

    def _get_graphql_url(self) -> str:
        """
        Generates the graphql endpoint.
        """
        __graphql_url = f'{self.url}/graphql/'
        result = urlparse(__graphql_url)
        if result.scheme and not SCHEMA_REGEX.match(__graphql_url):
            raise AttributeError(
                f'Invalid URL: {self.url}. Perhaps you meant `http://...` or `https://...`?')
        if not result.scheme or not result.netloc:
            raise AttributeError(f'url {self.url} is incorrect')
        return __graphql_url

    async def __execute__query(self, query: str, variables: dict = None):
        """
        Execute query
        """
        _client = await self._get_client()
        async with _client as session:
            graphql_client = AioGraphQLClient(
                self.__graphql_url, session=session)
            _response = await graphql_client.execute(query, variables=variables)
            response = await _response.json()
        return response

    def execute_query(self, query: str, variables: dict = None):
        """
        Execute query with query param.
        :param query: Query that needs to be executed
        :param variables: Dictionary of variables that are used inside the query.
        """

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.__execute__query(query, variables))
        except (RuntimeError, Exception) as e:
            self.logger.error(f"Error occurred = {e}")

    async def execute_async_query(self, query: str, variables: dict = None):
        """
        Execute query asynchronously.
        :param query: Query that needs to be executed
        :param variables: Dictionary of variables that are used inside the query.
        :return:
        """
        try:
            return await self.__execute__query(query, variables)
        except (RuntimeError, Exception) as e:
            self.logger.error(f"Error occurred = {e}")
