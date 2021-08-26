import aiohttp
from aiogqlc import GraphQLClient as AioGraphQLClient
import asyncio
from typing import Optional, Union
import validators


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
            raise AttributeError('Need to provide either username and password or oauth token')
        self.url = url
        self.username = username
        self.password = password
        self.token = token
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.__graphql_url = self._get_graphql_url()

    async def _get_client(self):
        _client_opts = {}
        if self.username and self.password:
            _opts = {
                'login': self.username,
                'password': self.password,
                'encoding': 'utf-8',
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
                _client_opts.update(timeout=aiohttp.ClientTimeout(total=self.timeout))
        _client_opts['connector'] = aiohttp.TCPConnector(ssl=self.verify_ssl)
        return aiohttp.ClientSession(**_client_opts)

    def _get_graphql_url(self) -> str:
        """
        Generates the graphql endpoint.
        """
        __graphql_url = f'{self.url}/graphql/'
        if not validators.url(__graphql_url):
            raise AttributeError(f'url entered is not correct = {self.url}')
        return f'{self.url}/graphql/'

    async def __execute__query(self, query: str):
        """
        Execute query
        """
        _client = await self._get_client()
        async with _client as session:
            graphql_client = AioGraphQLClient(self.__graphql_url, session=session)
            _response = await graphql_client.execute(query)
            response = await _response.json()
        return response

    def execute_query(self, query: str):
        """
        Execute query with query param.
        :param query: Query that needs to be executed
        """

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.__execute__query(query))
        except (RuntimeError, Exception) as e:
            print(f"Error occurred = {e}")
