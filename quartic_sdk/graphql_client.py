import aiohttp
import json, os
import requests
from aiogqlc import GraphQLClient as AioGraphQLClient
import asyncio
import nest_asyncio
import logging
import coloredlogs
from quartic_sdk._version import __version__
from typing import Optional, Union
from urllib.parse import urljoin
from urllib.parse import urlparse
import re
from quartic_sdk.api.api_helper import APIHelper
from quartic_sdk.utilities.constants import OAUTH, BASIC
from quartic_sdk.utilities.exceptions import IncorrectAuthTypeException
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.utilities.decorator import save_token, async_authenticate_with_tokens, get_and_save_token

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
        self.access_token = get_and_save_token(self.__graphql_url,username,password,verify_ssl)
        self.logger = logging.getLogger()
        coloredlogs.install(level='DEBUG', logger=self.logger)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        nest_asyncio.apply()

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
        
        _client_opts['headers'] = {'Authorization': f"Bearer {self.access_token}"}

        if self.timeout:
            if isinstance(self.timeout, aiohttp.ClientTimeout):
                _client_opts.update(timeout=self.timeout)
            else:
                _client_opts.update(
                    timeout=aiohttp.ClientTimeout(total=self.timeout))
        _client_opts['connector'] = aiohttp.TCPConnector(ssl=self.verify_ssl)
        _client_opts['raise_for_status'] = True
        return aiohttp.ClientSession(**_client_opts)

    def _get_graphql_url(self) -> str:
        """
        Generates the graphql endpoint.
        """
        __graphql_url = urljoin(self.url, "/graphql/")
        result = urlparse(__graphql_url)
        if result.scheme and not SCHEMA_REGEX.match(__graphql_url):
            raise AttributeError(
                f'Invalid URL: {self.url}. Perhaps you meant `http://...` or `https://...`?')
        if not result.scheme or not result.netloc:
            raise AttributeError(f'url {self.url} is incorrect')
        return __graphql_url
    
    @async_authenticate_with_tokens
    async def __execute__query(self, query: str, variables: dict = None):
        """
        Execute query
        """
        _client = await self._get_client()
        async with _client as session:
            graphql_client = AioGraphQLClient(
                self.__graphql_url, session=session)
            _response = await graphql_client.execute(query, variables=variables)
            _response.raise_for_status()
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

    @staticmethod
    def get_graphql_client_from_apihelper(api_helper: APIHelper):
        """
        Returns an instance of GraphqlClient from provided
        api_helper instance.
        :param api_helper: APIHelper instace whose configurations will be used to initialte GraphqlClient
        :return: new GraphqlCleint instance initiated with existing APIHelper configuration. 
        """
        configuration = api_helper.configuration
        if configuration.auth_type == OAUTH:
            return GraphqlClient(url=configuration.gql_host,
            token=configuration.oauth_token,
            verify_ssl=configuration.verify_ssl)

        elif configuration.auth_type == BASIC:
            return GraphqlClient(url=configuration.gql_host,
            username=configuration.username,
            password=configuration.password,
            verify_ssl=configuration.verify_ssl)    
        else:
            raise IncorrectAuthTypeException('Only OAUTH and BASIC auth_types are supported')

